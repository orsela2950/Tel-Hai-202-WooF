// Function to fetch and display TOML data
async function fetchAndDisplayTOML() {
  try {
    // Fetch the TOML file
    const response = await fetch('/pages/Logs/main.toml');
    if (!response.ok) {
      throw new Error(`Error fetching TOML file: ${response.statusText}`);
    }

    // Parse the TOML content
    const tomlContent = await response.text();
    const parsedData = toml.parse(tomlContent);

    // Display the data in the DOM
    displayData(parsedData);
  } catch (error) {
    console.error('Error fetching or displaying TOML data:', error);
  }
}

// Function to display data in the DOM
function displayData(data) {
  // Assuming 'data' is an object, you can customize this based on your TOML structure
  const tomlDataElement = document.getElementById('tomlData');
  tomlDataElement.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

// Fetch and display the TOML file when the page loads, ensuring toml is available
if (typeof toml !== 'undefined') {
  document.addEventListener('DOMContentLoaded', fetchAndDisplayTOML);
} else {
  console.error('TOML library not loaded. Ensure the script tag is included correctly.');
}