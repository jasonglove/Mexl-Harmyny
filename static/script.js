function findRecipe() {
    // Get the URL input value
    var urlInput = document.getElementById('url').value;

    // Create a new FormData object
    var formData = new FormData();
    formData.append('url-input', urlInput);

    // Send a POST request to the Flask route '/find-recipe'
    fetch('/find-recipe', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Check if the status is success
        if (data.status === 'success') {
            // Display ingredients and directions
            var outputContainer = document.getElementById('outputContainer');
            outputContainer.innerHTML = "<h2>Ingredients:</h2>" + data.ingredients + "<h2>Directions:</h2>" + data.directions;
        } else {
            // Display error message
            var outputContainer = document.getElementById('outputContainer');
            outputContainer.innerHTML = "<p>Error: " + data['status-code'] + "</p>";
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
