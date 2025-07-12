# ⚡ WattsUp – Energy Spike Anomaly Detection

**WattsUp** is an end-to-end machine learning project designed to detect abnormal energy spikes from smart meter data using time-series forecasting and anomaly detection. The project includes an ML-powered backend, an interactive frontend dashboard, and real-time anomaly detection using live energy data streams.

---

## 🚀 Features

- ✅ Abnormal energy usage detection using **Isolation Forest**
- ✅ Time series forecasting using **Facebook Prophet**
- ✅ Upload your own **CSV** energy data to check for anomalies
- ✅ Interactive and responsive dashboard using **Chart.js**
- ✅ Real-time **energy stream visualization** with live updates
- ✅ Highlight anomalies dynamically in **red** on the usage graph
- ✅ Toggle for **dark/light mode**, anomalies, zoom, and filters
- ✅ Download options for **PNG**, **PDF**, and **CSV**
- ✅ Real-time anomaly table with cause tooltips

---

## 🧠 How It Works

1. **Data Ingestion**: Upload or stream smart meter energy data  
2. **Preprocessing**: Resample, clean, and format data  
3. **Forecasting**: Predict expected energy usage using Prophet  
4. **Anomaly Detection**: Identify spikes using Isolation Forest  
5. **Visualization**: Show anomalies and patterns using interactive charts  
6. **Streaming**: Visualize live energy data and detect anomalies on the fly  

---

## 🗂️ Folder Structure
```
wattsup/
│
├── data/ # Raw and processed energy data
│ └── processed_with_anomalies.csv
│
├── model/ # Trained machine learning models
│ └── isolation_forest.pkl
│
├── notebooks/ # Jupyter notebooks for EDA and modeling
│ ├── forecasting_prophet.ipynb
│ └── anomaly_detection_iforest.ipynb
│
├── app/ # Flask application code
│ ├── static/ # JS, CSS, and Chart.js configurations
│ │ ├── style.css
│ │ └── chart.js
│ ├── templates/ # HTML templates
│ │ └── index.html
│ └── app.py # Main Flask backend
│
├── requirements.txt # Python dependencies
└── README.md # Project documentation

yaml
Copy
Edit
```
---

## 📅 Day-wise Contribution Log

### ✅ Day 1 – Project Setup

- Initialized GitHub repository  
- Created modular folder structure for data, models, app, and notebooks  

---

### ✅ Day 2 – Time Series Forecasting

- Cleaned and resampled electricity usage data  
- Performed EDA with trend visualizations  
- Trained **Facebook Prophet** for 30-day forecasting  
- Plotted forecast with confidence intervals and components  
- Saved forecast notebook  

---

### ✅ Day 3 – Anomaly Detection

- Trained **Isolation Forest** with 1% contamination  
- Labeled abnormal spikes in energy usage  
- Visualized anomalies using Matplotlib  
- Saved model and output with anomaly labels  

---

### ✅ Day 4 – Web App Development

- Built Flask web application with CSV upload  
- Integrated **Chart.js** for interactive charts  
- Added:
  - Anomaly toggle  
  - Zoom, pan, and reset  
  - Dark/light theme switch  
  - Download options: PNG, PDF, CSV  
  - Data table and custom date filters  

---

### ✅ Day 5 – Real-Time Streaming

- Integrated **Socket.IO** for real-time backend-to-frontend streaming  
- Plotted live usage with streaming updates  
- Detected and displayed live anomalies in red  
- Enhanced tooltips with anomaly cause  
- Added live anomaly table  

---

## 🌱 Future Improvements

| Feature | Description |
|--------|-------------|
| ✅ User Authentication | Login/signup to track personal data |
| ✅ Multivariate Anomaly Detection | Add weather, appliances, external features |
| ✅ Model Retraining | Allow model retraining with new data |
| ✅ REST API Support | For third-party integrations |
| ✅ Scheduled Forecasting | Auto-run daily/weekly predictions |
| ✅ Email/SMS Alerts | Trigger alerts on critical spikes |
| ✅ Threshold Controls | Let users customize anomaly criteria |
| ✅ JSON Upload API | Support IoT-based uploads |
| ✅ Mobile Responsive UI | Optimize dashboard for phones/tablets |
| ✅ Docker Deployment | Containerize with Docker |
| ✅ Database Integration | Use PostgreSQL or MongoDB for persistence |

---

## 🛠️ Tech Stack

| Tool            | Purpose                          |
|-----------------|----------------------------------|
| Python          | Data processing, ML training     |
| Pandas & NumPy  | Data manipulation                |
| Scikit-learn    | Isolation Forest anomaly model   |
| Facebook Prophet| Time series forecasting          |
| Flask           | Backend web server & routing     |
| Socket.IO       | Real-time streaming              |
| Chart.js        | Frontend chart visualization     |
| Bootstrap       | UI styling                       |
| Render/Railway  | Deployment platforms             |

---

## 🧪 Try It Yourself

```bash
git clone https://github.com/yourusername/wattsup.git
cd wattsup
pip install -r requirements.txt
python app/app.py
