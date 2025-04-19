from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import traceback
import logging
from concurrent.futures import ThreadPoolExecutor
import syntok.segmenter as segmenter
from argostranslate import translate
import translation_models

# Install models
translation_models.install()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files (e.g., HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

# Reload installed languages from install_translation_models
installed_languages = translate.get_installed_languages()
lang_de = next(lang for lang in installed_languages if lang.code == "de")
lang_en = next(lang for lang in installed_languages if lang.code == "en")

translation_de_en = lang_de.get_translation(lang_en)
translation_en_de = lang_en.get_translation(lang_de)

if translation_de_en is None or translation_en_de is None:
    raise RuntimeError("One or both translation directions could not be loaded correctly.")

class TranslationRequest(BaseModel):
    text: str
    direction: str  # "de-en" or "en-de"

def split_into_sentences(text: str):
    sentences = []
    for paragraph in segmenter.process(text):
        for sentence in paragraph:
            sentences.append("".join(token.value for token in sentence))
    return sentences

def translate_sentences(sentences, translator):
    translations = []
    for sentence in sentences:
        logger.info(f"Processing sentence: {sentence}")
        translations.append(translator.translate(sentence))
    return translations

def parallel_translate(text, translator):
    sentences = split_into_sentences(text)
    logger.info(f"Will process {len(sentences)} sentence(s) in parallel.")
    with ThreadPoolExecutor(max_workers=150) as executor:
        futures = []
        for i, sentence in enumerate(sentences):
            logger.info(f"Submitting translation task {i+1}/{len(sentences)}")
            futures.append(executor.submit(translate_sentences, [sentence], translator))
        results = [future.result()[0] for future in futures]
    return " ".join(results)

def perform_translation(request: TranslationRequest):
    if request.direction == "de-en":
        translator = translation_de_en
    elif request.direction == "en-de":
        translator = translation_en_de
    else:
        raise HTTPException(status_code=400, detail="Invalid direction (use 'de-en' or 'en-de')")

    try:
        return {"translation": parallel_translate(request.text, translator)}
    except Exception as e:
        logger.error(f"Translation failed:\n" + traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post("/translate-cpu")
def translate_cpu(request: TranslationRequest):
    return perform_translation(request)

@app.post("/translate-gpu")
def translate_gpu(request: TranslationRequest):
    return perform_translation(request)
