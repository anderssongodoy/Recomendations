import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

# Generar datos simulados
data = []
for _ in range(1000):  # Generar 1000 clientes simulados
    data.append({
        "customer_id": fake.uuid4(),
        "category": np.random.choice(["Electrodomésticos", "Limpieza", "Alimentos", "Ropa", "Tecnología", "Belleza"]),
        "purchase_date": fake.date_this_year(),
        "amount_spent": round(np.random.normal(100, 50), 2),  # Distribución normal con media 100, desviación estándar 50
        "num_purchases": np.random.randint(1, 10),  # Número de compras realizadas
    })

# Crear DataFrame
df = pd.DataFrame(data)

# Limpiar datos: eliminar valores negativos en gastos
df['amount_spent'] = df['amount_spent'].apply(lambda x: max(x, 10))

# Guardar datos simulados en un archivo CSV
df.to_csv("simulated_data.csv", index=False)
print("Datos simulados generados y guardados en 'simulated_data.csv'")
