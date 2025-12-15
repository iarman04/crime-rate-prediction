async function loadYearlyTrends() {
    const res = await fetch('/api/yearly_trends');
    const data = await res.json();

    const ctx = document.getElementById('yearlyChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.Year),
            datasets: [{
                label: 'Total Crimes',
                data: data.map(d => d.TotalCrimes),
                borderColor: 'red',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            scales: { y: { beginAtZero: true } }
        }
    });
}

async function loadCrimeTypes() {
    const res = await fetch('/api/crime_types');
    const data = await res.json();

    const ctx = document.getElementById('typesChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.Type),
            datasets: [{
                label: 'Count',
                data: data.map(d => d.Count),
                backgroundColor: 'blue'
            }]
        },
        options: {
            scales: { y: { beginAtZero: true } }
        }
    });
}

async function loadDistricts(year) {
    const res = await fetch(`/api/district_crimes/${year}`);
    const data = await res.json();

    const ctx = document.getElementById('districtChart').getContext('2d');
    if (window.districtChartInstance) {
        window.districtChartInstance.destroy();
    }
    window.districtChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => `District ${d.District}`),
            datasets: [{
                label: 'Crimes',
                data: data.map(d => d.CrimeCount),
                backgroundColor: 'green'
            }]
        },
        options: {
            scales: { y: { beginAtZero: true } }
        }
    });
}