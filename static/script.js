document.getElementById('predictionForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevents the form from submitting in the traditional way

    const form = event.target;
    const formData = new FormData(form);

    // Create a JSON object from the form data
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = parseFloat(value); // Convert string values to numbers
    });

    const resultElement = document.getElementById('predictionResult');
    resultElement.textContent = 'Predicting...';

    try {
        const response = await fetch('http://127.0.0.1:5000/predict_crop', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Something went wrong');
        }

        const data = await response.json();
        
        // Display the prediction result
        resultElement.textContent = data.predicted_crop;

    } catch (error) {
        resultElement.textContent = `Error: ${error.message}`;
        console.error('Error:', error);
    }
});