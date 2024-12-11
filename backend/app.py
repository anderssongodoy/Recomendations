from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import hashlib
import random

app = Flask(__name__)
CORS(app)

# Cargar datos simulados
df = pd.read_csv("simulated_data.csv")

# Codificar categorías
df['category_encoded'] = LabelEncoder().fit_transform(df['category'])
features = df[['amount_spent', 'category_encoded']]

# Entrenar el modelo k-NN
knn = NearestNeighbors(n_neighbors=3, metric='euclidean')
knn.fit(features)

def get_consistent_recommendations(customer_id, num_recommendations=3):
    """
    Genera recomendaciones consistentes basadas en el customer_id.
    """
    # Crear un hash del customer_id para obtener un número único
    hash_value = int(hashlib.sha256(customer_id.encode()).hexdigest(), 16)
    
    # Usar el hash para generar índices consistentes
    indices = hash_value % len(df)
    
    # Seleccionar filas específicas basadas en los índices
    consistent_rows = df.iloc[indices:indices + num_recommendations].reset_index()
    recommendations = consistent_rows[["category", "amount_spent"]].to_dict(orient='records')
    
    return recommendations

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    # Obtener el customer_id de la solicitud
    data = request.json
    customer_id = data.get('customer_id', None)
    
    if not customer_id:
        return jsonify({"error": "Customer ID is required"}), 400

    # Filtrar los datos del cliente específico
    customer_row = df[df['customer_id'] == customer_id]
    if customer_row.empty:
        return jsonify({"error": "Customer ID not found"}), 404

    # Obtener las características del cliente
    customer_data = customer_row[['amount_spent', 'category_encoded']].values.reshape(1, -1)
    
    # Calcular las recomendaciones con k-NN
    distances, indices = knn.kneighbors(customer_data)

    # Obtener recomendaciones
    recommendations = df.iloc[indices[0]][['category', 'amount_spent']].to_dict(orient='records')
    return jsonify({"customer_id": customer_id, "recommendations": recommendations})

@app.route('/category-details', methods=['GET'])
def get_category_details():
    # Obtener la categoría desde los parámetros de la URL
    category = request.args.get('category', None)
    
    if not category:
        return jsonify({"error": "Category is required"}), 400

    # Filtrar productos basados en la categoría
    category_products = df[df['category'] == category]
    
    if category_products.empty:
        return jsonify({"error": f"No data found for category: {category}"}), 404

    # Seleccionar algunos productos de la categoría
    products = category_products.sample(n=min(5, len(category_products))).reset_index()
    product_list = [
        {
            "name": f"{category} Producto {i+1}",
            "price": row['amount_spent']
        }
        for i, row in products.iterrows()
    ]

    # Generar promociones relacionadas
    promotions = [
        f"Descuento {random.randint(10, 50)}% en productos de {category}.",
        f"Compra 2 y lleva 1 gratis en {category}.",
        f"Envío gratis para compras de {category} superiores a $50."
    ]

    # Respuesta del endpoint
    return jsonify({
        "category": category,
        "products": product_list,
        "promotions": promotions
    })


if __name__ == '__main__':
    app.run(debug=True)
