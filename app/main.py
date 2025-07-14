import sys
import os
import time
import pandas as pd
from flask import Flask, render_template, request, jsonify
from functools import lru_cache
from flask_socketio import SocketIO, emit
import google.generativeai as genai
import shap
import eventlet

# Fix Python path so we can import from parent directory modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import SHAP explanation and feature loader
from model.shap_explainer import get_shap_explanation_for_index, precompute_shap_for_anomalies
from data.load_features import load_features

# Configure eventlet for WebSocket
eventlet.monkey_patch()

# Configure Gemini API
<<<<<<< HEAD
# It is strongly recommended to load the API key from an environment variable for security.
# Example: genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyAQc6Y-vomCUSdz1w8y5SuP9wzazdqCWEg"))  # Replace with env var for production
=======
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
>>>>>>> e2bdb23051e2b5a83dba7653e7e29ef014312186

# Initialize Flask App
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

DATA_DIR = '../data/'
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
        _, features_df = load_features()
        explanation = get_shap_explanation_for_index(index, features_df)
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
        df = pd.read_csv('../data/live_energy.csv')
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

# This function can be cached because its arguments are simple, hashable types.
@lru_cache(maxsize=128)
def fetch_gemini_insight(usage, timestamp):
    """
    Fetches insight from the Gemini API. This function is cached to avoid
    repeated calls for the same data and to help with rate limiting.
    """
    prompt = (
        f"The following energy usage was recorded: {usage} kWh at {timestamp}. "
        f"In one sentence, explain whether this usage is normal or abnormal for a household."
    )
    # Switch to gemini-1.0-pro, which has a more generous free tier (e.g., 60 RPM)
    # and is well-suited for this kind of simple text generation task.
    model = genai.GenerativeModel(model_name='gemini-pro')
    response = model.generate_content(prompt)
    return response.text.strip()

# AI Insight using Gemini
@app.route('/insight', methods=['POST'])
def get_insight():
    data = request.get_json()
    usage = data.get("energy_usage", 0)
    timestamp = data.get("timestamp", "unknown")
    
    # Round usage to make caching more effective for similar values
    rounded_usage = round(usage, 1)

    try:
        explanation = fetch_gemini_insight(rounded_usage, timestamp)
        return jsonify({"insight": explanation})
    except Exception as e:
        print("Gemini error:", e)
        error_message = str(e)
        if "quota" in error_message.lower() or "429" in error_message:
            return jsonify({"insight": "⚠️ AI insight is temporarily unavailable due to high demand. Please try again in a minute."}), 429
        return jsonify({"insight": f"⚠️ Could not fetch AI insight: {error_message}"}), 500

# Run Flask App
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)
