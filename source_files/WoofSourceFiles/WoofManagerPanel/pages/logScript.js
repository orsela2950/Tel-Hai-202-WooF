// Import the 'toml' library using ES module syntax
import * as toml from 'https://cdn.skypack.dev/toml';

// Function to fetch and display TOML data
async function fetchAndDisplayTOML() {
  try {
    // Fetch the TOML file
    const response = await fetch('./Logs/main.toml');
    if (!response.ok) {
      throw new Error(`Error fetching TOML file: ${response.statusText}`);
    }

    // Parse the TOML content
    const tomlContent = await response.text();
    const parsedData = toml.parse(tomlContent);

    // Make a deep copy of the parsed data to avoid redefining keys issue
    const copiedData = JSON.parse(JSON.stringify(parsedData));

    // Display logs in a table
    displayLogsTable(copiedData);

  } catch (error) {
    console.error('Error fetching or displaying TOML data:', error);
  }
}

// Function to display logs in a table
function displayLogsTable(parsedData) {
  // Assuming parsedData is your JSON object with the "logs" key
  const logTableBody = document.getElementById('log-table-body');

  parsedData.logs.forEach(logEntry => {
    const row = document.createElement('tr');

    // Assuming you want to display certain properties in the table
    const propertiesToDisplay = ['timestamp', 'request_method', 'client_host', 'url', 'target_url'];

    propertiesToDisplay.forEach(prop => {
      const cell = document.createElement('td');
      cell.textContent = logEntry[prop];
      row.appendChild(cell);
    });

    logTableBody.appendChild(row);
  });
}

// Fetch and display the TOML file when the page loads
document.addEventListener('DOMContentLoaded', async () => {
  try {
    await fetchAndDisplayTOML();
  } catch (error) {
    console.error('Error during page load:', error.message || error);
  }
});
