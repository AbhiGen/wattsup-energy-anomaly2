from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import pandas as pd
import os
import time

# Initialize Flask + SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Required for WebSocket

DATA_DIR = '../data/'
DEFAULT_MODEL = 'isolation_forest'  # Change to 'lof' or 'ocsvm' if needed

@app.route('/')
def index():
    return render_template('index.html')  # Loads your HTML dashboard

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        print("DEBUG: No file in request.files")
        return jsonify({'error': 'No file uploaded'}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        print("DEBUG: Uploaded file has no name")
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Load uploaded file
        df = pd.read_csv(uploaded_file)
        print("DEBUG: CSV columns received:", df.columns.tolist())

        # Rename 'date' column to 'timestamp' if needed
        if 'date' in df.columns:
            df.rename(columns={'date': 'timestamp'}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Load corresponding model output file
        model_file_path = os.path.join(DATA_DIR, f'{DEFAULT_MODEL}_output.csv')
        model_df = pd.read_csv(model_file_path)
        print("DEBUG: Model file columns:", model_df.columns.tolist())

        if 'date' in model_df.columns:
            model_df.rename(columns={'date': 'timestamp'}, inplace=True)
        model_df['timestamp'] = pd.to_datetime(model_df['timestamp'])

        # Find a model-specific anomaly column (e.g., 'iso_anomaly')
        anomaly_col = None
        for col in model_df.columns:
            if 'anomaly' in col and col not in ['score', 'anomaly']:
                anomaly_col = col
                break

        if not anomaly_col:
            raise Exception("No model anomaly column found")

        print("DEBUG: Using anomaly column:", anomaly_col)

        # Rename model anomaly column to prevent conflict
        model_df.rename(columns={anomaly_col: 'model_anomaly'}, inplace=True)

        # Merge and assign unified 'anomaly' column
        merged = pd.merge(df, model_df[['timestamp', 'model_anomaly']], on='timestamp', how='left')
        merged['anomaly'] = merged['model_anomaly'].fillna(0).astype(int)

        # Prepare JSON response
        response_data = merged[['timestamp', 'energy_usage', 'anomaly']].copy()
        response_data['timestamp'] = response_data['timestamp'].dt.strftime('%Y-%m-%d')
        return jsonify(response_data.to_dict(orient='records'))

    except Exception as e:
        print("DEBUG: Error loading/merging model data:", e)
        return jsonify({'error': str(e)}), 500

# =======================
# 🔌 WebSocket Live Stream
# =======================
@socketio.on('start_stream')
def stream_data():
    print("⚡ Stream started")
    try:
        df = pd.read_csv('../data/live_energy.csv')
        for _, row in df.iterrows():
            usage = float(row['energy_usage'])
            anomaly = 1 if usage > 120 or usage < 90 else 0  # Basic rule-based anomaly

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
        print("❌ Error during stream:", e)
        emit('error', {'message': str(e)})


# =============
# Run the App
# =============
if __name__ == '__main__':
    socketio.run(app, debug=True)  # Use socketio.run instead of app.run
