# ArgosOpenTech Translator German ↔ English

Simple REST API for German ↔ English translation using Argos models.


| Repository                                                                                    | Speed                                  | Translation Quality | Notes                                         |
|-----------------------------------------------------------------------------------------------|----------------------------------------|---------------------|-----------------------------------------------|
| [facebook-nllb-translator-api-py](https://github.com/jmaycon/facebook-nllb-translator-api-py) | 🚶‍♂️ Slowest                          | ✅ Best              | Accurate translations, but slower performance |
| [marian-translator-api-py](https://github.com/jmaycon/marian-translator-api-py)               | 🏃 Faster than NLLB, slower than Argos | 👍 Good             | Balanced between quality and speed            |
| [argos-translator-api-py](https://github.com/jmaycon/argos-translator-api-py)                 | ⚡ Fastest                              | ⚠️ Lower            | Extremely fast but less accurate              |

---

## Run

### Option 1: Run with Docker 🐳

UI: http://localhost:30000/

```shell
docker build -t argos-translator-api-py .
docker run --rm -p 30000:8080 argos-translator-api-py 
```

### Option 2: On Linux

UI: http://localhost:30001/

```shell
chmod +x run_local.sh
./run_local.sh
```

### Option 2: On Windows (PowerShell)

UI: http://localhost:30002/

```shell
./run_local.ps1
```

---

## 🔁 API Usage

It seems Argos Translate is built on top of CTranslate2, which does support GPU execution.

### POST `/translate`

Translate text between German and English.

`direction` options:

- `"de-en"` = German → English
- `"en-de"` = English → German

#### Sample Request (with curl)

1.German to English

```shell
curl -X POST http://localhost:30000/translate \
      -H "Content-Type: application/json" \
      -d '{"text": "Guten Morgen", "direction": "de-en"}'
```

- 2.English to German

```shell
curl -X POST http://localhost:30000/translate \
      -H "Content-Type: application/json" \
      -d '{"text": "Hi my friend", "direction": "en-de"}'
```

#### Sample Response

```json
{
  "translation": "Good morning"
}
```

---

## 🧩 Models Used

- https://github.com/argosopentech/argos-translate



