from flask import Flask, request, render_template_string, redirect
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded.csv'

# Load CSV file


def load_data():
    if os.path.exists(UPLOAD_FOLDER):
        return pd.read_csv(UPLOAD_FOLDER)
    return pd.read_csv("labeled_traffic.csv")

# Generate anomaly chart over time


def generate_chart(df):
    if 'second_frame' not in df.columns:
        return None

    grouped = df.groupby('second_frame')['is_anomaly'].mean() * 100
    fig, ax = plt.subplots(figsize=(14, 5))  # Increased width

    grouped.plot(ax=ax, kind='line', title="📈 Anomaly % over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("Anomaly %")
    ax.grid(True)
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')


@app.route('/', methods=['GET', 'POST'])
def index():
    # Upload handling
    if request.method == 'POST' and 'csv_file' in request.files:
        file = request.files['csv_file']
        if file and file.filename.endswith('.csv'):
            file.save(UPLOAD_FOLDER)
            return redirect('/')

    df = load_data()

    # Stats
    total_packets = len(df)
    total_anomalies = df['is_anomaly'].sum(
    ) if 'is_anomaly' in df.columns else 0
    anomaly_percentage = (
        total_anomalies / total_packets * 100) if total_packets else 0

    # Table
    table_html = df.to_html(
        classes='table table-bordered table-striped', index=False)

    # Chart
    chart_data = generate_chart(df)

    # HTML template
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Network Anomaly Dashboard</title>
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/css/bootstrap.min.css">
        <style>
            .anomaly-row {
                background-color: #f8d7da !important;
                color: #721c24;
            }
            body {
                background-color: #f5f5f5;
                padding: 2rem;
                font-family: sans-serif;
            }
            .stats, .upload-box {
                background: #fff;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                border-left: 5px solid #007bff;
            }
            .chart {
                margin-top: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>📡 Network Traffic Dashboard</h2>

            <div class="upload-box">
                <form method="post" enctype="multipart/form-data">
                    <label>📁 Upload new CSV:</label>
                    <input type="file" name="csv_file">
                    <button class="btn btn-sm btn-primary">Upload</button>
                </form>
            </div>

            <div class="stats">
                <strong>Total Packets:</strong> {{ total_packets }}<br>
                <strong>Total Anomalies:</strong> {{ total_anomalies }}<br>
                <strong>Anomaly Rate:</strong> {{ anomaly_percentage }}%
            </div>

            {{ table|safe }}

            {% if chart_data %}
            <div class="chart">
                <h4>📊 Anomaly Rate Over Time</h4>
                <img src="data:image/png;base64,{{ chart_data }}" class="img-fluid">
            </div>
            {% endif %}
        </div>

        <script>
            // Highlight anomaly rows
            const table = document.querySelector("table");
            const headers = Array.from(table.querySelectorAll("th")).map(th => th.innerText.trim());
            const anomalyIndex = headers.indexOf("is_anomaly");

            if (anomalyIndex !== -1) {
                const rows = table.querySelectorAll("tbody tr");
                rows.forEach(row => {
                    const cells = row.querySelectorAll("td");
                    if (cells[anomalyIndex]?.innerText.trim() === "1") {
                        row.classList.add("anomaly-row");
                    }
                });
            }

            // Auto refresh
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = 'autorefresh';
            checkbox.style.marginLeft = '10px';

            const label = document.createElement('label');
            label.innerHTML = ' 🔁 Auto Refresh';
            label.prepend(checkbox);
            document.querySelector('.stats').appendChild(label);

            checkbox.addEventListener('change', function () {
                if (this.checked) {
                    localStorage.setItem('autorefresh', 'true');
                    setInterval(() => location.reload(), 10000);
                } else {
                    localStorage.removeItem('autorefresh');
                }
            });

            if (localStorage.getItem('autorefresh') === 'true') {
                checkbox.checked = true;
                setInterval(() => location.reload(), 10000);
            }
        </script>
    </body>
    </html>
    '''

    return render_template_string(
        html,
        table=table_html,
        total_packets=total_packets,
        total_anomalies=total_anomalies,
        anomaly_percentage=round(anomaly_percentage, 2),
        chart_data=chart_data
    )


if __name__ == '__main__':
    app.run(debug=True)
