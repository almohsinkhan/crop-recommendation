# app.py

from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle

# Create a Flask app instance
app = Flask(__name__)

# Load the trained model, scaler, and label encoder
# Make sure 'model.pkl', 'scaler.pkl', and 'le.pkl' are in the same directory
try:
    model = pickle.load(open('model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    le = pickle.load(open('le.pkl', 'rb')) # Make sure to save your label encoder as well!
except FileNotFoundError:
    print("Error: One or more pickle files not found. Ensure 'model.pkl', 'scaler.pkl', and 'le.pkl' are in the same directory.")
    exit()

@app.route('/')
def home():
    return render_template('index.html')


# Define the prediction endpoint
@app.route('/predict_crop', methods=['POST'])
def predict_crop():
    """
    API endpoint to predict the best crop based on input parameters.
    """
    try:
        # Get the JSON data from the request
        data = request.get_json(force=True)

        # Extract features from the JSON data, ensuring the order is correct
        features = [
            data['N'], 
            data['P'], 
            data['K'], 
            data['temperature'], 
            data['humidity'], 
            data['ph'], 
            data['rainfall']
        ]

        # Convert features to a NumPy array and reshape for the scaler
        input_data = np.array([features])
        
        # Scale the input data using the pre-fitted scaler
        scaled_data = scaler.transform(input_data)
        
        # Make a prediction using the model
        prediction_encoded = model.predict(scaled_data)
        
        # Inverse transform the numerical prediction back to the crop name
        predicted_crop_name = le.inverse_transform(prediction_encoded)
        
        # Return the prediction as a JSON response
        return jsonify({
            'predicted_crop': predicted_crop_name[0]
        })
    
    except KeyError as e:
        return jsonify({'error': f"Missing key in JSON input: {e}"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)