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
// quiz_script.js

document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Collect form data
        const formData = new FormData(form);

        // Send form data to the server using AJAX
        fetch('/save_quiz_answers', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error in saving quiz answers');
            }
            
        })
        .then(() => {
            // Handle successful response (if needed)
            console.log('Quiz answers saved successfully');
            // You can redirect or perform any other action here
            
        })
        .catch(error => {
            // Handle errors
            console.error('Error:', error);
            // You can show an error message or perform any other action here
        });
    });
});
