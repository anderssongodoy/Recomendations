from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Cargar datos simulados
df = pd.read_csv("simulated_data.csv")

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    # Obtener el customer_id de la solicitud
    data = request.json
    customer_id = data.get('customer_id', None)
    
    if not customer_id:
        return jsonify({"error": "Customer ID is required"}), 400
    
    # Generar recomendaciones ficticias (a futuro usaremos IA)
    recommendations = df.sample(3)[["category", "amount_spent"]].to_dict(orient='records')
    return jsonify({"customer_id": customer_id, "recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
