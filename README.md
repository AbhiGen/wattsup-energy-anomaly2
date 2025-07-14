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
project_root/
├── app/
│   ├── static/
│   └── templates/
│       └── index.html
├── main.py
├── data/
│   ├── __pycache__/
│   │   └── load_features.cpython-312.pyc
│   ├── __init__.py
│   ├── features.csv
│   ├── isolation_forest_output.csv
│   ├── live_energy.csv
│   ├── load_features.py
│   ├── lof_anomalies.csv
│   ├── ocsvm_anomalies.csv
│   ├── processed_with_anomalies.csv
│   └── test_data.csv
├── model/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── isolation_forest.pkl
│   ├── shap_explainer.py
├── notebooks/
├── .gitignore
├── README.md
└── render.yaml
yaml
Copy
Edit
```
---



## 2. **Problem Definition & Understanding**

In many rural communities, erratic power consumption patterns and undetected energy anomalies result in increased costs, damaged equipment, and poor energy planning. These anomalies can go unnoticed due to lack of real-time monitoring tools and predictive intelligence. Addressing this issue is critical for promoting energy resilience, affordability, and efficient planning in resource-constrained settings. Detecting energy spikes and consumption irregularities can reduce outages, optimize load distribution, and support the deployment of renewable microgrids. Our solution provides a way to detect these spikes early using ML models, ensuring proactive energy management for rural households and institutions.

---

## 3. **Design Approaches Explored**

We explored multiple techniques:

* **Threshold-based detection**: Simple, but not adaptable to seasonal/time-based usage changes.
* **Statistical Z-score anomaly detection**: Sensitive to noise; poor in identifying non-linear patterns.
* **Machine Learning models (e.g., Isolation Forest, LOF, OCSVM)**: Good performance but needs preprocessing.
* **Deep Learning (LSTMs)**: High accuracy but requires large datasets and high compute.

**Chosen:** Hybrid approach using Facebook Prophet for forecasting and Isolation Forest for anomalies — offering a balance of accuracy, interpretability, and deployment feasibility.

---

## 4. **Best-Fit Solution Chosen & Rationale**

We selected a lightweight ML stack combining **Facebook Prophet** for time-series forecasting and **Isolation Forest** for anomaly detection. This approach handles seasonal and temporal energy variations while being computationally efficient. It allows real-time and batch data processing, supports custom CSV uploads, and visualizes anomalies interactively. The system suits low-resource environments and can be deployed easily in web or mobile interfaces, empowering rural users and administrators with real-time energy insights.

---

## 5. **Design Process**

We followed the **Design Thinking approach**:

1. **Empathize**: Identified challenges from rural electrification use cases.
2. **Define**: Targeted the problem of undetected energy spikes.
3. **Ideate**: Explored various forecasting and anomaly detection models.
4. **Prototype**: Built a modular, interactive Flask-based web app.
5. **Test**: Validated with simulated and uploaded energy datasets.

Participatory inputs from community energy experts and academic mentors shaped our model parameters and interface design.

---

## 6. **Architecture of the Proposed Solution**

**Core Components:**

* **Frontend**: HTML + Chart.js dashboard (Dark/Light toggle, filters, zoom, download options).
* **Backend**: Flask + Python (REST endpoints, model orchestration).
* **Forecasting Module**: Facebook Prophet for trend and seasonal prediction.
* **Anomaly Detector**: Isolation Forest model with adjustable contamination.
* **Real-Time Streaming**: Socket.IO for live visualization and updates.
* **Visualization**: Highlight anomalies in red, export PNG/PDF/CSV.

**Technology Stack**: Python, Pandas, Scikit-learn, Prophet, Flask, Chart.js, Bootstrap, Socket.IO

> !\[Optional: Insert architecture diagram or system sketch here]

---

## 7. **Target Audience / Beneficiaries**

* **Primary Users**:

  * Rural households with smart meters
  * Village-level grid operators
  * Microgrid providers and energy cooperatives

* **Secondary Users**:

  * Researchers and NGOs monitoring rural energy sustainability
  * Students and energy innovation hubs

---

## 8. **Scalability Vision**

WattsUp is modular and deployable on cloud (Render/Railway) or edge (Raspberry Pi) setups. It uses open-source technologies and is trained on customizable thresholds, making it easily adaptable across geographies and datasets. With scheduled retraining and REST API integration, it can support community-scale deployments and integrate with renewable systems. Planned enhancements include:  

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
