

def search_vector(client, vector, top_k=5):
    db = client["Tradercom"]
    collection = db["TraderProduct"]
    # define pipeline
    pipeline = [
        {
            '$vectorSearch': {
            'index': 'vector_index', 
            'path': 'DataEmbedding', 
            'queryVector': vector, 
            'numCandidates': 150, 
            'limit': 150
            }
        }, {
            '$project': {
            '_id': 0, 
            'TN': 1,
            'TNP': 1, 
            'Info': 1, 
            'Images': 1,
            'ProviderCategory': 1,
            'score': {
                '$meta': 'vectorSearchScore'
            }
            }
        }
    ]

    # run pipeline
    result = collection.aggregate(pipeline)
    return result

if __name__ == "__main__":
    import mongo_conection
    # from vector_data import data
    from queries_products import select_product

    print ("Iniciando el vector_search")
    client = mongo_conection.connect_to_mongo()
    data = select_product("NBC197375758015", client)
    result = search_vector(client, data[0]['DataEmbedding'])
    # print(f"Cantidad de resultados: {len(result)}")
    # print results
    TN = ''
    for i in result:
        if i['TNP'] != TN:
            TN = i['TNP']
            print(i['Images'][0]['Url'] + " - " + str(i['score']) + " - " + i['TNP'] + " - " + i['ProviderCategory'])
    print ("Fin del vector_search")