// Sample data for charts
const engagementData = {
    x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    y: [1000, 1500, 2000, 1800, 2500, 3000],
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Engagement'
};

const platformData = [{
    values: [30, 25, 20, 25],
    labels: ['Twitter', 'Facebook', 'Instagram', 'LinkedIn'],
    type: 'pie'
}];

Plotly.newPlot('engagementChart', [engagementData], {
    title: 'Engagement Trends',
    margin: { t: 30, b: 40, l: 40, r: 30 }
});

Plotly.newPlot('platformChart', platformData, {
    title: 'Platform Distribution',
    margin: { t: 30, b: 40, l: 40, r: 30 }
}); 