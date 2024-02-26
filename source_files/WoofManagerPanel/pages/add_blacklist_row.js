// Function to submit the form and add a new blacklist row
function submitForm() {
    const ipAddress = document.getElementById('ipAddress').value;
    const reason = document.getElementById('reason').value;
    const expirationDate = document.getElementById('expirationDate').value;
    const source = "manager panel";

    // You can perform validation on the form data here if needed

    // Send the form data to the server
    fetch('/add-blacklist-row', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ipAddress,
            reason,
            expirationDate,
            source,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Server response:', data);
        // Check the response and take appropriate actions
        if (data.success) {
            // Row added successfully
            showAlert('Row added successfully!', 'green');
            // You can close the form, redirect, or perform any other action
        } else {
            // Server response indicates an error
            showAlert(`Error: ${data.message}`, 'red');
            // You can handle the error, display a message, or take other actions
        }
    })
    .catch(error => {
        console.error('Error adding new row:', error);
        // Handle other errors, such as network issues
    });
}

// Function to display an alert with specified text and color
function showAlert(message, color) {
    const alertDiv = document.getElementById('alert');
    alertDiv.textContent = message;
    alertDiv.style.color = color;
    alertDiv.style.display = 'block';

    // Hide the alert after a certain duration (e.g., 3 seconds)
    setTimeout(() => {
        alertDiv.style.display = 'none';
    }, 3000);
}