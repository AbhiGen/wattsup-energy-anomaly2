# ⚡ WattsUp – Energy Spike Anomaly Detection

An end-to-end Machine Learning project to detect abnormal energy spikes from smart meter data using ML algorithms. The project includes a trained model, an interactive web dashboard, and deployment.

---

## 🚀 Features

- Detect abnormal usage spikes in energy data  
- Visualize spikes using an interactive dashboard  
- Upload CSV files to check for anomalies  
- Real-time energy monitoring with live anomaly detection  
- Deployable web application

---

## 🧰 Tech Stack

- **Python** – Data processing, ML training  
- **Flask** – Web server and API  
- **Pandas, NumPy** – Data manipulation  
- **Scikit-learn** – ML model (Isolation Forest)  
- **Chart.js** – Frontend chart visualization  
- **Bootstrap** – UI styling  
- **Socket.IO** – Real-time data streaming  
- **Deployment** – Render / Railway / Replit



## 📁 Folder Structure

```
wattsup/
│
├── data/ # Raw and processed energy data
├── model/ # Trained ML model files (.pkl)
├── notebooks/ # Jupyter notebooks for EDA and modeling
├── app/ # Flask backend and frontend code
│ ├── static/ # JavaScript, CSS, Chart.js config
│ ├── templates/ # HTML templates
│ └── app.py # Main Flask app
└── README.md # Project documentation

```

## ✅ Progress Log

### ✅ Day 1 – Setup

- Initialized GitHub repository  
- Created base project folder structure  

---

### ✅ Day 2 – Time Series Forecasting

- Performed time series forecasting using Facebook Prophet  
- Cleaned and resampled electricity usage data to daily totals  
- Conducted Exploratory Data Analysis (EDA)  
  - Plotted daily electricity consumption over time  
- Trained time series forecasting model  
- Forecasted energy usage for next 30 days  
- Plotted results with confidence intervals  
- Analyzed weekly and trend components  
- Saved forecasting notebook to GitHub  

---

### ✅ Day 3 – Anomaly Detection using Isolation Forest

- Trained **Isolation Forest** with 1% contamination (outlier detection)  
- Detected and labeled abnormal energy spikes  
- Saved:  
  - `model/isolation_forest.pkl` – Trained model  
  - `data/processed_with_anomalies.csv` – Output with anomaly labels  
- Visualized spikes using Matplotlib  

---

### ✅ Day 4 – Web App with Visualization

🔧 Built an interactive **Flask web application** to visualize electricity usage and detected anomalies.

#### 💡 Features:
- **CSV Upload Support**  
- **Interactive Chart** using Chart.js  
  - Anomalies highlighted in **red**  
  - Moving Average line  
- **Dark/Light Mode Toggle**  
- **Anomaly Toggle**: Show/hide anomalies  
- **Zoom & Pan Controls**  
  - Mouse wheel / pinch zoom  
  - Navigation buttons (← ↑ ↓ →)  
  - Reset zoom  
- **Download Options**  
  - 📄 Export chart as **PNG**  
  - 📕 Export dashboard as **PDF**  
  - 📊 Download anomalies as **CSV**  
- **Anomaly Table** below chart  
- **Date Filter**: Custom date range filter for chart and table  

---

### ✅ Day 5 – Real-Time Streaming & Live Anomaly Table

📡 Added **real-time live stream** using WebSockets (Socket.IO)

#### ⚙️ Live Stream Features:
- Stream energy data in real-time from backend to frontend  
- Detect anomalies instantly from streamed data  
- Plot **live usage chart** with real-time updates  
- Anomalies appear as red points on the chart  
- **Tooltip Enhancements**  
  - Show anomaly cause on hover  
- ✅ Added **Live Anomaly Table**  
  - Updates dynamically as anomalies are detected  

---
