const ctx = document.getElementById('trafficChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Upload (KB/s)', data: [], borderColor: 'red', fill: false },
            { label: 'Download (KB/s)', data: [], borderColor: 'blue', fill: false }
        ]
    },
    options: {
        animation: false,
        scales: {
            x: { display: false },
            y: { beginAtZero: true }
        }
    }
});

const source = new EventSource('/stats');
source.onmessage = function(event) {
    const data = JSON.parse(event.data);
    chart.data.labels.push('');
    chart.data.datasets[0].data.push((data.sent / 1024).toFixed(2));
    chart.data.datasets[1].data.push((data.recv / 1024).toFixed(2));
    if (chart.data.labels.length > 20) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[1].data.shift();
    }
    chart.update();
};
