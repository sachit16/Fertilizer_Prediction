// Function to fetch prediction result from the backend
function fetchPredictionResult(prediction) {
    fetch('/result/' + prediction)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); // Parse response as text
    })
    .then(data => {
        // Display the prediction result in the 'result' div
        document.getElementById('result').innerHTML = data;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

// Function to submit the form and handle prediction result
function submitForm() {
    // Get form data
    const formData = new FormData(document.getElementById('inputForm'));

    // Make a POST request to the '/predict' endpoint with form data
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text(); // Parse response as text
    })
    .then(data => {
        // Fetch prediction result after form submission
        fetchPredictionResult(data);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

// Function to clear the form fields
function clearForm() {
    document.getElementById("inputForm").reset();
}
