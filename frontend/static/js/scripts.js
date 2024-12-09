async function getRecommendations() {
    const customerID = document.getElementById('customer_id').value;

    // Validar si se ingresó un ID
    if (!customerID) {
        alert('Por favor, ingrese un ID de cliente.');
        return;
    }

    try {
        const response = await fetch('/recommendations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ customer_id: customerID })
        });

        if (!response.ok) {
            throw new Error('Error al obtener recomendaciones.');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        alert('Hubo un problema al procesar la solicitud: ' + error.message);
    }
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (data.recommendations && data.recommendations.length > 0) {
        data.recommendations.forEach(rec => {
            const categoryDiv = document.createElement('div');
            categoryDiv.classList.add('category');
            categoryDiv.textContent = `Categoría: ${rec.category}`;

            const detailsLink = document.createElement('a');
            detailsLink.href = `/details.html?category=${rec.category}`;
            detailsLink.textContent = ' Ver detalles';
            detailsLink.style.marginLeft = '10px';

            const recommendationDiv = document.createElement('div');
            recommendationDiv.appendChild(categoryDiv);
            recommendationDiv.appendChild(detailsLink);

            resultsDiv.appendChild(recommendationDiv);
        });
    } else {
        resultsDiv.textContent = 'No se encontraron recomendaciones.';
    }
}
