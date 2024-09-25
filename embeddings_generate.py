import torch # Librería para trabajar con tensores de PyTorch.
import clip # Librería para cargar el modelo CLIP preentrenado.
import pickle # Libreria para guardar objetos en archivos binarios en el disco.
import numpy as np
from PIL import Image # Librería para cargar y procesar imágenes.
from dowload_image import download_image

def get_model(use_local_model=True):
    if use_local_model is False:
        return clip.load("ViT-B/32", device="cpu")
    # Cargar el modelo CLIP desde un archivo. Se utiliza el objeto precargao usando el "store_model.py".
    print("Cargando modelo CLIP desde un archivo")
    with open("modelo_clip.pkl", "rb") as f:
        loaded_model = pickle.load(f)
    return loaded_model

# El resultado es un tensor de 512 dimensiones (puedes usarlo como embedding)
def get_embedding_image(image_path, loaded_model):
    # Cargar el modelo CLIP preentrenado
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ## model, preprocess = clip.load("ViT-B/32", device=device)
    model, preprocess = loaded_model

    image = download_image(image_path)
    if image is None:
        return None

    # Preprocesar la imagen
    image_input = preprocess(image).unsqueeze(0).to(device)

    # Obtener el embedding de la imagen
    with torch.no_grad():
        image_embedding = model.encode_image(image_input)
    if image_embedding is None:
        return None
    return image_embedding.numpy().tolist()[0]

def get_embedding_text(text, loaded_model):
    # Cargar el modelo CLIP desde un archivo. Se utiliza el objeto precargao usando el "store_model.py".
    ### loaded_model = get_model()

    # Cargar el modelo CLIP preentrenado
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ## model, preprocess = clip.load("ViT-B/32", device=device)
    model, preprocess = loaded_model

    # Preprocesar el texto
    text_input = clip.tokenize(text).to(device)

    # Obtener el embedding del texto
    with torch.no_grad():
        text_embedding = model.encode_text(text_input)
    if text_embedding is None:
        return None
    return text_embedding.numpy().tolist()[0]


if __name__ == "__main__":
    loaded_model = get_model(use_local_model=False)
    image_path = "https://trcmnbco.s3.amazonaws.com/M1080AFF_1.jpg"
    image_embedding = get_embedding_image(image_path, loaded_model)
    if image_embedding is None:
        print("Error generando el embedding de la imagen: ", image_path)
        exit(1)
    print("Embedding de la imagen: (",len(image_embedding),")")

    text_token = "Lifestyle_Calzado_Hombre_Tenis_Shifted"
    text_embedding = get_embedding_text(text_token, loaded_model)
    if text_embedding is None:
        print("Error generando el embedding del texto: ", text_token)
        exit(1)
    print("Embedding del texto (", len(text_embedding), "):")

    # Los embeddings se combinan pero no aumenta de dimension, se sumam y siguen siendo de 512 dimensiones.
    combined_embedding = np.add(image_embedding, text_embedding)
    print("Embedding combinado (", len(combined_embedding), "):")
    print(combined_embedding)