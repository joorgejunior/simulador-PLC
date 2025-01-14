// Carregar dados e inicializar elementos
fetch('/data')
    .then(response => response.json())
    .then(data => {
        // Dados do gráfico
        const chartData = data.chart_data;
        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Sample Data',
                    data: chartData.values,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false
                }]
            }
        });

        // Dados do mapa
        const mapData = data.map_data;
        const map = L.map('map').setView([mapData.latitude, mapData.longitude], 12);

        // Adicionar tiles do OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Adicionar marcador ao mapa
        L.marker([mapData.latitude, mapData.longitude]).addTo(map)
            .bindPopup('Localização estática')
            .openPopup();
    });
