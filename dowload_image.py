import requests
import os
from PIL import Image

def download_image(url):
    try:
        local_path = "images/image.jpg"
        delete_file(local_path)
        response = requests.get(url)
        with open(local_path, "wb") as f:
            f.write(response.content)
        image = Image.open(local_path)
        return image

    except Exception as e:
        # print(e)
        return None

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

if __name__ == "__main__":
    url = "https://i.ibb.co/5R7zDd2/image.jpg"
    image = download_image(url)
    if image is None:
        print("Error al descargar la imagen ubicada en:", url)
        exit(1)
    image.show()
