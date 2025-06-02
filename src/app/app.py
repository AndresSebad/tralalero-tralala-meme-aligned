import gradio as gr
from PIL import Image
import random
import time
import torch
from transformers import LlavaNextForConditionalGeneration, AutoProcessor
from peft import PeftModel
import spaces

MODEL_ID = 'llava-hf/llava-v1.6-mistral-7b-hf'
ADAPTER_ID = 'AndresSebad/llava-v1.6-mistral-7b-memes-chilenos-small'

processor = AutoProcessor.from_pretrained(MODEL_ID)
processor.tokenizer.padding_side = "right"

model_nuevo = LlavaNextForConditionalGeneration.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto"
)
model_nuevo = PeftModel.from_pretrained(model_nuevo, ADAPTER_ID)
model_nuevo = model_nuevo.eval()

@spaces.GPU
def explicar_meme_stream(img: Image.Image):
    if img is None:
        yield "❌ No hay imagen para analizar."
        return

    img = img.convert("RGB")
    img = img.resize((336, 336))

    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": "Eres experto en memes chilenos. Observa la imagen y, si hay texto, interprétalo sin repetirlo. Analiza su sentido usando contexto cultural chileno. Responde según la instrucción."},
                {"type": "text", "text": "Explica qué significa este meme en Chile, usando lenguaje coloquial chileno."},
            ],
        }
    ]

    text_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
    inputs = processor(text=text_prompt, images=[img], return_tensors="pt").to(model_nuevo.device)

    with torch.no_grad():
        generated_ids = model_nuevo.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            pixel_values=inputs["pixel_values"],
            image_sizes=inputs["image_sizes"],
            max_new_tokens=256
        )

    respuesta = processor.batch_decode(generated_ids[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True)[0]

    # Simula stream de escritura
    for i in range(1, len(respuesta) + 1):
        yield respuesta[:i]
        time.sleep(0.02)

def cargar_imagen_ejemplo(nombre: str) -> Image.Image:
    if nombre == "🐶 Perro confundido existencialmente":
        return Image.open("perro.png")
    elif nombre == "🎉 Perro 18 con espíritu patriótico":
        return Image.open("perro18.png")
    elif nombre == "🛝 Resbalín":
        return Image.open("resbalin.jpg")
    elif nombre == "🍷 Santa Helena":
        return Image.open("santa.jpg")

def limpiar_selector():
    return gr.update(value=None)
    
BANNER_URL = "tralalelo-tralala-logo.png"

with gr.Blocks(theme=gr.themes.Base(), title="LLaVA Chile Memes") as demo:
    
    gr.Image(value=BANNER_URL, show_label=False, interactive=False, elem_id="banner", height=200, width=300)

    gr.Markdown(
        """
        # 🇨🇱 Tralalelo Tralala Meme Align  
        *¿Qué quiso decir este meme chileno?*  
        Sube un meme o elige uno de nuestros clásicos, y nuestro modelo entrenado con cariño te explicará el chiste con contexto cultural local.
        """
    )

    with gr.Row():
        with gr.Column():
            ejemplo_selector = gr.Radio(
                label="🎯 O elige un clásico perruno:",
                choices=["🐶 Perro confundido existencialmente", "🎉 Perro 18 con espíritu patriótico"],
                interactive=True
            )

            input_img = gr.Image(type="pil", label="📷 Sube tu meme chileno o elige uno arriba", height=336, width=336)
            output_label = gr.Textbox(label="🧠 Explicación cultural", interactive=False)

            input_img.change(fn=lambda: "", inputs=None, outputs=output_label)
            ejemplo_selector.change(fn=cargar_imagen_ejemplo, inputs=ejemplo_selector, outputs=input_img)

            btn = gr.Button("👀 Explica el meme")
            btn.click(fn=explicar_meme_stream, inputs=input_img, outputs=output_label)

    gr.Markdown(
        """
        --- 
        **Repositorio del modelo:** [`AndresSebad/llava-v1.6-mistral-7b-memes-chilenos-small`](https://huggingface.co/AndresSebad/llava-v1.6-mistral-7b-memes-chilenos-small)  
        """
    )

if __name__ == "__main__":
    demo.launch()
