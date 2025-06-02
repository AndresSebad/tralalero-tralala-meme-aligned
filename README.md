# Tralalelo-Tralala-Meme-Align 
**Hackathon Somos NLP 2025** 

<img src="./tralalelo-tralala-logo.png" alt="Descripción" width="450" height="250"/>

> Fine-tuning de **LLaVA-Next** con 1194 memes chilenos.

🔗 [Demo en Gradio](https://huggingface.co/spaces/somosnlp-hackathon-2025/tralalelo-tralala-demo). 
🔗 [Modelo en Hugging Face](https://huggingface.co/somosnlp-hackathon-2025/llava-v1.6-mistral-7b-memes-chilenos-small).  
🔗 [Dataset con memes chilenos](https://huggingface.co/datasets/somosnlp-hackathon-2025/memes_instagram_chilenos_es_small).

---

## 1 · Descripción

Demostramos que un modelo multimodal puede **entender y explicar humor local**.

Partimos de **LLaVA-Next** y lo adaptamos con un dataset propio de **700 memes chilenos** (imagen + texto + 4 776 explicaciones). 

---

## 2 · Estructura del repo

```
├── data/
│   ├── raw/        
│   └── processed/  
├── notebooks/
│   ├── create_dataset.ipynb
│   └── save_data.ipynb
├── src/
│   ├── train/        
│   └── app/        
│       ├── app.py
│       └── requirements.txt
├── Makefile        
└── README.md
```

---

## 3 · Puesta en marcha rápida

```bash
make init                       
source .venv/bin/activate       
huggingface-cli login           
```

---

## 4 · Dataset

| Notebook | Descripción |
|----------|-------------|
| **create_dataset.ipynb** | Define cuentas de Instagram, descarga memes con **Apify** y guarda metadatos. |
| **save_data.ipynb**      | Lee el Excel procesado, limpia y sube el dataset a Hugging Face. |

---

## 5 · Variables de entorno

Antes de ejecutar la app o scripts, asegúrate de tener un archivo `.env` en la raíz del proyecto con las siguientes claves:

```
OPENAI_API_KEY=tu_clave_openai
APIFY_TOKEN=tu_token_apify
HF_TOKEN=tu_token_huggingface
```

---

## 6 · Entrenamiento

- Script en `src/train/`
- Ejecutado en GPU **L40S**
- Fine-tuning con **LoRA (PEFT)**
- Hiperparámetros:
  - r = 8 · alpha = 8 · dropout = 0.1
  - batch = 1 · accumulate = 8 · epochs = 2
- Métrica: `bert_score` (maxima)

---

## 7 · Demo Gradio

Edita el código en `src/app/`. Para desplegarlo:

```bash
make push_app_hf SPACE_ID=andressebastian/tralalelo-tralala-demo
```
