import datetime
import numpy as np

def select_products(provider_name, client):
    """Seleccina un segmento de productos de la base de datos"""
    try:
        db = client["Tradercom"]
        collection = db["TraderProduct"]
        cursor = collection.find(
            {"ProviderName": provider_name, "DataEmbedding": [], "StatusGeneric":'Published'}, 
            {"_id": 0, "TN": 1, "Info": 1, "Images": 1, "ProviderCategory": 1} 
        ).limit(500)
        # cursor = collection.find({"TN": "NBC197375748641"}, {"_id": 0, "TN": 1, "Info": 1, "Images": 1, "ProviderCategory": 1}).limit(1)
        list_products = []

        for document in cursor:
            list_products.append(create_product(document))
        return list_products

    except Exception as e:
        print(f"query_products.select_Products: Error al seleccionar los productos: {e}")

def select_product(tn, client):
    """Seleccina un segmento de productos de la base de datos"""
    try:
        db = client["Tradercom"]
        collection = db["TraderProduct"]
        cursor = collection.find({"TN": tn}, {"_id": 0, "TN": 1, "Info": 1, "Images": 1, "ProviderCategory": 1, "DataEmbedding": 1}).limit(1)
        list_products = []

        for document in cursor:
            product = create_product(document)
            product['DataEmbedding'] = document['DataEmbedding']
            list_products.append(product)
        return list_products

    except Exception as e:
        print(f"query_products.select_Products: Error al seleccionar los productos: {e}")

def update_embedding(client, tn, embedding):
    try: 
        db = client["Tradercom"]
        collection = db["TraderProduct"]
        
        result = collection.update_one({"TN": tn}, {"$set": {"DataEmbedding": embedding}})
        # print(f"query_products.update_embedding: Embedding actualizado: {result.matched_count} documento(s) actualizado(s)")
        return result.matched_count > 0 
    except Exception as e:
        print(f"query_products.update_embedding: Error al actualizar el embedding: {e}")


def create_product(document):
    image_data = ''
    for image in document.get('Images'):
        if image.get('ImagenTypeId') == 1:
            image_data = image.get('Url')
            break

    return {
            "ProductName": document.get('Info')[0].get('ProductName'),
            "TN": document.get('TN'),
            "ProductShortDescription": document.get('Info')[0].get('ProductShortDescription'),
            "ImageUrl": image_data,
            "ProviderCategory": document.get('ProviderCategory'),
            "brandName": document.get('brandName'),
            "upc": document.get('upc'),
        }

def custom_datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")  # Formato personalizado
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


if __name__ == "__main__":
    import mongo_conection

    client = mongo_conection.connect_to_mongo()
    method = "no-seleccionado-en-el-menu"
    #method = "query_products"
    method = "select_product"
    # method = "update_embedding"

    if method == "select_product":
        print("Iniciando el select_product")
        list_products = select_product("NBC197375748641", client)
        if len(list_products) == 0:
            print("No se encontraron resultados")
        for product in list_products:
            print(product)
    if method == "query_products":
        print("Iniciando el query_products")
        list_products = select_products("NewBalanceCO", client) 
        if len(list_products) == 0:
            print("No se encontraron resultados")
        for product in list_products:
            print(product['ProviderCategory'])
        # print(list_products if len(list_products) > 0 else "No se encontraron resultados") 
    elif method == "update_embedding":
        print("Iniciando el update_embedding")
        client = mongo_conection.connect_to_mongo()
        result = update_embedding(client, "NBC197375748641", [0.1, 0.2, 0.3])
        print(result)
    else:
        print("Descomenta alguno de los dos metodos...")
