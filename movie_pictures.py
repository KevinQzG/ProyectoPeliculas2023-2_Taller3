#importar librerías
import os
import openai
import json
from dotenv import load_dotenv, find_dotenv
import requests
from PIL import Image
from io import BytesIO
import numpy as np

#Se lee del archivo .env la api key de openai
_ = load_dotenv('openAI.env')
openai.api_key  = os.environ['openAI_api_key']

#Se carga la lista de películas de movie_titles.json
with open('movie_descriptions.json', 'r') as file:
    file_content = file.read()
    movies = json.loads(file_content)

idx_movie = np.random.randint(len(movies)-1)
print(movies[idx_movie])

# Se hace la conexión con la API de generación de imágenes. El prompt en este caso es:
# "Genera una escena original de la película [nombre de la película]"
response = openai.Image.create(
  prompt=f"Genera una escena original de la película {movies[np.random.randint(idx_movie)]['title']}",
  n=1,
  size="512x512"
)
image_url = response['data'][0]['url']


# La API devuelve la url de la imagen, por lo que debemos generar una función auxiliar que
# descargue la imagen.
def fetch_image(url):
    response = requests.get(url)
    response.raise_for_status()

    # Convert the response content into a PIL Image
    image = Image.open(BytesIO(response.content))
    return(image)

img = fetch_image(image_url)
img.show()