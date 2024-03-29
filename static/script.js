function findRecipe() {

    var loadingIcon = document.getElementById('loadIcon');
    var hiddenElements = document.getElementById('hiddenElements');
    hiddenElements.style.display = 'none';
    loadingIcon.style.display = 'block';

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
            var foodImage = document.getElementById("foodImage")
            outputContainer.innerHTML = data.newRecipe;
            console.log(data.imageurl)
            foodImage.src = data.imageurl;
            hiddenElements.style.display = 'block';
            loadingIcon.style.display = 'none';
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

// document.addEventListener("DOMContentLoaded", function() {
//     const form = document.querySelector('form');

//     form.addEventListener('submit', function(event) {
//         event.preventDefault(); // Prevent the default form submission

//         // Collect form data
//         const formData = new FormData(form);

//         // Send form data to the server using AJAX
//         fetch('/save_quiz_answers', {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Error in saving quiz answers');
//             }
            
//         })
//         .then(() => {
//             // Handle successful response (if needed)
//             console.log('Quiz answers saved successfully');
//             // You can redirect or perform any other action here
            
//         })
//         .catch(error => {
//             // Handle errors
//             console.error('Error:', error);
//             // You can show an error message or perform any other action here
//         });
//     });
// });
