import eventlet
eventlet.monkey_patch()

import sys
import os
import time
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import google.generativeai as genai
import shap

# Fix Python path so we can import from parent directory modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import SHAP explanation and feature loader
from model.shap_explainer import get_shap_explanation_for_index, precompute_shap_for_anomalies
from data.load_features import load_features

# Configure eventlet for WebSocket
# eventlet.monkey_patch() # This line is now moved to the top

# Configure Gemini API - get from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Initialize Flask App
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# Use absolute paths relative to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
DEFAULT_MODEL = 'isolation_forest'

# Main Dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Upload CSV & Merge
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        df = pd.read_csv(uploaded_file)
        if 'date' in df.columns:
            df.rename(columns={'date': 'timestamp'}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        model_file_path = os.path.join(DATA_DIR, f'{DEFAULT_MODEL}_output.csv')
        if not os.path.exists(model_file_path):
            return jsonify({'error': f"Model output file not found at {model_file_path}"}), 400

        model_df = pd.read_csv(model_file_path)

        if 'date' in model_df.columns:
            model_df.rename(columns={'date': 'timestamp'}, inplace=True)
        model_df['timestamp'] = pd.to_datetime(model_df['timestamp'])

        anomaly_col = None
        for col in model_df.columns:
            if 'anomaly' in col and col not in ['score', 'anomaly']:
                anomaly_col = col
                break

        if not anomaly_col:
            raise Exception("No model anomaly column found")

        model_df.rename(columns={anomaly_col: 'model_anomaly'}, inplace=True)
        merged = pd.merge(df, model_df[['timestamp', 'model_anomaly']], on='timestamp', how='left')
        merged['anomaly'] = merged['model_anomaly'].fillna(0).astype(int)

        # Pre-compute SHAP explanations for anomalies
        try:
            _, features_df = load_features()
            anomaly_indices = merged[merged['anomaly'] == -1].index.tolist()
            precompute_shap_for_anomalies(anomaly_indices)
        except Exception as e:
            print(f"Warning: Could not pre-compute SHAP explanations: {e}")

        response_data = merged[['timestamp', 'energy_usage', 'anomaly']].copy()
        response_data['timestamp'] = response_data['timestamp'].dt.strftime('%Y-%m-%d')
        return jsonify(response_data.to_dict(orient='records'))

    except Exception as e:
        print("DEBUG: Error:", e)
        return jsonify({'error': str(e)}), 500

# SHAP Explanation API Route
@app.route('/api/explain/<int:index>')
def explain(index):
    try:
        explanation = get_shap_explanation_for_index(index)
        return jsonify({
            "index": index,
            "explanation": explanation
        })
    except Exception as e:
        print(f"SHAP Explanation error for index {index}: {e}")
        return jsonify({"error": str(e)}), 500

# Live WebSocket Stream
@socketio.on('start_stream')
def stream_data():
    print("⚡ Stream started")
    try:
        live_data_path = os.path.join(DATA_DIR, 'live_energy.csv')
        df = pd.read_csv(live_data_path)
        for _, row in df.iterrows():
            usage = float(row['energy_usage'])
            anomaly = 1 if usage > 120 or usage < 90 else 0

            cause = ""
            if anomaly:
                cause = "Very High Usage" if usage > 120 else "Very Low Usage"

            socketio.emit('live_data', {
                'timestamp': row['timestamp'],
                'energy_usage': usage,
                'anomaly': anomaly,
                'cause': cause
            })

            socketio.sleep(2)
    except Exception as e:
        print("❌ Stream error:", e)
        emit('error', {'message': str(e)})

# AI Insight using Gemini
@app.route('/insight', methods=['POST'])
def get_insight():
    data = request.get_json()
    usage = data.get("energy_usage", 0)
    timestamp = data.get("timestamp", "unknown")

    prompt = (
        f"The following energy usage was recorded: {usage} kWh at {timestamp}. "
        f"In one sentence, explain whether this usage is normal or abnormal."
    )

    try:
        # Check if API key is available
        if not os.getenv("GEMINI_API_KEY"):
            return jsonify({"insight": "⚠️ AI insights unavailable - API key not configured"}), 200
            
        model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest')
        response = model.generate_content(prompt)
        explanation = response.text.strip()
        return jsonify({"insight": explanation})
    except Exception as e:
        print("Gemini error:", e)
        return jsonify({"insight": f"⚠️ Could not fetch AI insight: {e}"}), 500

# Health check endpoint for deployment
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "WattsUp API is running"})

# Run Flask App
if __name__ == '__main__':
    # Get port from environment variable for deployment compatibility
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)