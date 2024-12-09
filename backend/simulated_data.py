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
        "category": np.random.choice(["Electrodomésticos", "Limpieza", "Alimentos", "Ropa"]),
        "purchase_date": fake.date_this_year(),
        "amount_spent": round(np.random.uniform(10, 500), 2),
    })

# Crear DataFrame
df = pd.DataFrame(data)

# Guardar datos simulados en un archivo CSV
df.to_csv("simulated_data.csv", index=False)
print("Datos simulados generados y guardados en 'simulated_data.csv'")