import time
import mongo_conection
import numpy as np
from queries_products import select_products, update_embedding
from embeddings_generate import get_embedding_image, get_embedding_text, get_model

print ("Iniciando el programa")
try:
    client = mongo_conection.connect_to_mongo()
    print("Conectado a la base de datos")
    load_model = get_model(use_local_model=False)
    start_timer = time.time()
    # 1. Busca los productos de la base de datos.
    for provider in ["NewBalanceCO", "PilatosCO", "Mali", "Bamers", "TheNorthFaceCo", "BosiCO", "DieselCO", "ParisCL", "Prochampions", "RunningBalboa", "SteveMaddenCO", "SuperDryCO", ]:
        print(f"Procesando {provider}")
        accumulated_products = 0
        existProducts = True
        while existProducts:
            list_products = select_products(provider, client)
            if list_products is None or len(list_products) == 0:
                if accumulated_products == 0:
                    print("No se encontraron prouctos en la base de datos para procesar")
                else:
                    print(f"No se encontraron resultados después de {accumulated_products} productos procesados")
                existProducts = False
                break
            count = 0
            for product in list_products:
                count += 1
                # 2. Crea el embedding de cada producto.
                embdding_image = get_embedding_image(product["ImageUrl"], load_model)
                text_to_embed = f"{product["ProductName"]} {product["ProviderCategory"]} {product["brandName"]}"
                embdding_text = get_embedding_text(text_to_embed, load_model)
                combined_embedding = np.add(embdding_image, embdding_text)
                product["embedding"] = combined_embedding.tolist()
                ## print(f"Embedding de {product['TN']}: {product['embedding']}")
                if product["embedding"] is None:
                    print(f"Error generando el embedding de la imagen: {product['ImageUrl']}")
                    continue
                if count % 100 == 0:
                    print(f"Procesados {count + accumulated_products } de {len(list_products) + accumulated_products}")
                    end_timer = time.time()
                    print(f"Tiempo transcurrido: {end_timer - start_timer} segs")
                # 3. Actualiza el campo embedding en la base de datos.
                result = update_embedding(client, product["TN"], product["embedding"])
            accumulated_products += len(list_products)
    
except Exception as e:
    print(f"Error de ejecución: {e}")
else:
    print("Programa terminado")
finally:
    mongo_conection.close_mongo_connection(client)
    end_timer = time.time()
    print(f"Tiempo final de ejecución: {end_timer - start_timer} segs")
