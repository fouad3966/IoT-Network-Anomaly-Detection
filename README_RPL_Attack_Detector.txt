# Real-Time RPL Attack Detector in IoT Networks

This project is a real-time RPL (Routing Protocol for Low-power and Lossy Networks) attack detection system designed for IoT networks. It captures live network traffic, extracts relevant features per second, classifies activity using a machine learning model, and provides a web dashboard to monitor anomalies visually and statistically.

---

## 🛠 Features

- **Live Packet Sniffing**: Captures real-time packets using `scapy`.
- **Feature Extraction**: Calculates metrics per second like:
  - Total packet count
  - TCP/UDP packet count
  - Average packet size
- **Anomaly Detection**: Uses a trained ML model to classify each second's traffic as normal or anomalous.
- **Web Interface**: View traffic logs, overall stats, and charts of anomalies.
- **Export Logs**: CSV file updated with features and predictions in real time.

---

## 🖥️ Web Dashboard

- Table showing features and whether a time frame is anomalous.
- Total stats: total packets, anomalies, TCP/UDP distribution.
- Line chart for real-time anomaly detection over time.

---

## 🚀 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/RPL-Attack-Detector.git
cd RPL-Attack-Detector
```

### 2. Install Dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

Then install required packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install flask pandas scikit-learn scapy
```

### 3. Run the Detector

Start the real-time packet sniffer and anomaly detector:

```bash
python detector.py
```

This script will generate or update `labeled_traffic.csv` as packets are processed.

### 4. Launch the Web Dashboard

In a new terminal:

```bash
python app.py
```

Then go to `http://127.0.0.1:5000` in your browser to view the dashboard.

---

## 🧠 Model Training (Optional)

If you want to retrain or improve the model:

1. Use a labeled dataset of extracted features.
2. Train a model using `scikit-learn` or another ML library.
3. Save the model as `model.pkl` using `joblib` or `pickle`.

---

## 📌 Notes

- You may need to run as administrator or with `sudo` privileges to allow packet sniffing.
- This tool is for educational and research purposes and not meant for production use.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

- Mohamed Fouad Rabahi  
- Contributions welcome via pull requests.