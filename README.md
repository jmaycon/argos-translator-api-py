# Argos Translator German ↔ English

Simple REST API for German ↔ English translation using Argos models.

---

## 🖥️ Option 2: Run Locally

### 1. On Linux

UI will be available at http://localhost:30012/

```shell
chmod +x run_local.sh
./run_local.sh
```

### 2. On Windows (PowerShell)

Will be accessible at http://localhost:30013/

```shell
./run_local.ps1
```

## 🐳 Option 3: Run with Docker Compose

UI will be available at http://localhost:30014/

```shell
docker build -t argos-translator-api-py .
docker run --rm -p 30014:8080 argos-translator-api-py 
```

---

## 🔁 API Usage

To check if CUDA is available run

```shell
source venv/bin/activate
python -c "import torch; print(torch.cuda.is_available())"
```

_For powershell use `.\win-venv\Scripts\Activate.ps1`_

### POST `/translate-<cpu|gpu>`

Translate text between German and English.

`direction` options:

- `"de-en"` = German → English
- `"en-de"` = English → German

#### Sample Request (with curl)

1.German to English

```shell
curl -X POST http://localhost:30012/translate-cpu \
      -H "Content-Type: application/json" \
      -d '{"text": "Guten Morgen", "direction": "de-en"}'
```

- 2.English to German

```shell
curl -X POST http://localhost:30012/translate-cpu \
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



