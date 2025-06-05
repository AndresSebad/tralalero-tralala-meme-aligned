# Tralalelo-Tralala-Meme-Align

**Somos NLP Hackathon 2025**

<img src="./tralalelo-tralala-logo.png" alt="Description" width="450" height="250"/>

> Fine-tuning **LLaVA-Next** with 1194 Chilean memes.

🔗 [Demo on Gradio](https://huggingface.co/spaces/somosnlp-hackathon-2025/tralalero-tralala-demo)

🔗 [Model on Hugging Face](https://huggingface.co/somosnlp-hackathon-2025/llava-v1.6-mistral-7b-memes-chilenos-small)

🔗 [Dataset of Chilean Memes](https://huggingface.co/datasets/somosnlp-hackathon-2025/memes_instagram_chilenos_es_small)

---

## 1 · Description

We demonstrate that a multimodal model can **understand and explain local humor**.

We started with **LLaVA-Next** and adapted it using a custom dataset of **1194 Chilean memes** (image + text + 4776 explanations).

---

## 2 · Repository Structure

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

## 3 · Quick Start

```bash
make init                       
source .venv/bin/activate       
huggingface-cli login           
```

---

## 4 · Dataset

| Notebook                  | Description                                                                      |
| ------------------------- | -------------------------------------------------------------------------------- |
| **create\_dataset.ipynb** | Defines Instagram accounts, downloads memes using **Apify**, and saves metadata. |
| **save\_data.ipynb**      | Reads the processed Excel, cleans and uploads the dataset to Hugging Face.       |

---

## 5 · Environment Variables

Before running the app or any scripts, make sure you have a `.env` file in the project root with the following keys:

```
OPENAI_API_KEY=your_openai_key
APIFY_TOKEN=your_apify_token
HF_TOKEN=your_huggingface_token
```

---

## 6 · Training

* Script located in `src/train/`
* Trained on **L40S GPU**
* Fine-tuning using **LoRA (PEFT)**
* Hyperparameters:

  * r = 8 · alpha = 8 · dropout = 0.1
  * batch = 1 · accumulate = 8 · epochs = 2
* Metric: `bert_score` (maximize)

---

## 7 · Gradio Demo

Edit the code in `src/app/`. To deploy it:

```bash
make push_app_hf SPACE_ID=andressebastian/tralalelo-tralala-demo
```
