// Import the 'toml' library using ES module syntax
import * as toml from 'https://cdn.skypack.dev/toml';

// Function to handle row deletion
async function deleteRow(id) {
    try {
        // Send a request to the server to delete the row with the specified ID
        const response = await fetch(`/blacklist/${id}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error(`Error deleting row: ${response.statusText}`);
        }

        // Reload the table after deletion
        await fetchAndDisplayBlacklist();
    } catch (error) {
        console.error('Error deleting row:', error);
    }
}

// Function to fetch and display blacklist data
async function fetchAndDisplayBlacklist() {
    try {
        // Fetch the blacklist data from the server
        const response = await fetch('/blacklist');
        if (!response.ok) {
            throw new Error(`Error fetching blacklist data: ${response.statusText}`);
        }

        // Parse the JSON content
        const jsonData = await response.json();

        // Display blacklist data in the table
        displayBlacklistTable(jsonData);

    } catch (error) {
        console.error('Error fetching or displaying blacklist data:', error);
    }
}

// Function to display blacklist data in a table
function displayBlacklistTable(jsonData) {
    const blacklistTableBody = document.getElementById('blacklistTableBody');

    if (!blacklistTableBody) {
        console.error('Error: blacklistTableBody element not found.');
        return;
    }

    // Clear existing rows in the table
    blacklistTableBody.innerHTML = '';

    jsonData.blacklist.forEach(entry => {
        const row = document.createElement('li');
        row.className = 'table-row';

        const propertiesToDisplay = ['ip_address', 'reason', 'expiration_date', 'source'];

        // Add delete button to the row
        const deleteButtonCell = document.createElement('div');
        deleteButtonCell.className = 'col col-0';
        const deleteButton = document.createElement('button');
        deleteButton.innerHTML = '<ion-icon name="trash-outline" class="delete-button"></ion-icon>';
        deleteButton.addEventListener('click', () => deleteRow(entry.id));
        deleteButtonCell.appendChild(deleteButton);
        row.appendChild(deleteButtonCell);

        // Add other columns to the row
        propertiesToDisplay.forEach(prop => {
            const cell = document.createElement('div');
            cell.className = `col col-${propertiesToDisplay.indexOf(prop) + 1}`;

            // Format expiration_date
            if (prop === 'expiration_date') {
                const expirationDate = new Date(entry[prop]);
                cell.textContent = expirationDate.toLocaleString('en-GB', {
                    year: 'numeric',
                    month: 'numeric',
                    day: 'numeric',
                    hour: 'numeric',
                    minute: 'numeric',
                    second: 'numeric'
                });
            } else {
                cell.textContent = entry[prop];
            }

            row.appendChild(cell);
        });

        blacklistTableBody.appendChild(row);
    });
}

// Fetch and display the blacklist data when the page loads
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await fetchAndDisplayBlacklist();
    } catch (error) {
        console.error('Error during page load:', error.message || error);
    }
});