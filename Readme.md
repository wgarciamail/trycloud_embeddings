# Crea los embedding de los productos.

## Paso 1.
- Selecciona los productos para agregar el embedding.
- para cada producto:
    - Crea el embedding utilizando la imagen, titulo y escripcion.
    - Actualiza el campo el embedding.

## paso 2. 
- Crea el query que permita mediante un producto seleccionar los 100 productos similares.

## librerias:
```
%pip install git+https://github.com/openai/CLIP.git 
%pip install pillow
%pip install pymongo
```