# ⚡ WattsUp – Energy Spike Anomaly Detection

An end-to-end Machine Learning project to detect abnormal energy spikes from smart meter data using ML algorithms. The project includes a trained model, an interactive web dashboard, and deployment.

## 🚀 Features
- Detect abnormal usage spikes in energy data
- Visualize spikes using an interactive dashboard
- Upload CSV files to check for anomalies
- Deployable web application

## 🧰 Tech Stack
- Python, Pandas, NumPy, Scikit-learn
- ML: Isolation Forest, Time Series EDA
- Flask for backend
- HTML/CSS + Chart.js (for frontend visualization)
- Deployment via Render or Railway

## 📁 Folder Structure
- `data/` - contains raw and processed data
- `notebooks/` - Jupyter notebooks for EDA + modeling
- `model/` - trained ML model files
- `app/` - Flask backend and HTML templates

## ✅ Progress Log

### Day 1
- Initialized GitHub repository and base project folder structure

### Day 2
- Performed time series forecasting using Facebook Prophet
- Cleaned and resampled electricity usage data to daily totals
- Performed Exploratory Data Analysis (EDA)
    - Plotted daily electricity consumption over time
- Trained a time series model using Facebook Prophet
- Forecasted energy usage for the next 30 days
- Plotted forecast results including confidence intervals
- Analyzed trend and weekly patterns using Prophet components
- Saved the forecasting notebook to GitHub

### ✅ Day 3 – Anomaly Detection using Isolation Forest

- Cleaned and resampled daily energy usage data
- Trained **Isolation Forest** model with 1% anomaly threshold
- Detected and labeled abnormal spikes in electricity usage
- Saved:
  - Trained model (`model/isolation_forest.pkl`)
  - Labeled output (`data/processed_with_anomalies.csv`)
- Visualized spikes using Matplotlib

  # ✅ Day 4 – Web App with Visualization

🔧 Built an interactive **Flask web application** to visualize electricity usage and detected anomalies.
- **CSV Upload Support**: User uploads energy usage data via web interface.
- **Dynamic Chart Rendering**:
  - Used **Chart.js** to plot energy usage.
  - Anomalies (from Isolation Forest) marked in **red**.
- **Dark/Light Mode Toggle**: Theme switcher improves user accessibility.
- **Anomaly Toggle**: Show/hide anomaly points on the chart.
- **Zoom & Pan Controls**:
  - Enabled zooming and panning with mouse wheel and pinch gestures using `chartjs-plugin-zoom`.
- **Navigation Buttons**:
  - Move left/right/up/down on the chart
  - Zoom in/out buttons
  - Reset zoom button
- **Download Options**:
  - 📄 Export chart as **PNG**
  - 📊 Download anomalies as **CSV**
  - 📕 Export full dashboard view as **PDF**
- **Anomaly Table**:
  - Cleanly formatted anomaly list displayed under the graph
- **Date Filter**:
  - Apply a custom start/end date to filter the chart and table dynamically

