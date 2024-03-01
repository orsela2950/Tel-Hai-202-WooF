const form = document.getElementById('addBlacklistForm');
const popup = document.getElementById('popup');

form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission
    const formData = new FormData(form); // Get form data
    const data = Object.fromEntries(formData) // Convert to object
    console.log("addBlacklistForm data sent:")
    console.log(data)

    try {
      const response = await fetch('/add_blacklist_row', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        popup.style.display = 'block';
        setTimeout(() => {
          popup.style.display = 'none';
        }, 2000); // Hide popup after 2 seconds
      } else {
        let response_txt = await response.text()
        console.error('Error submitting data:', response_txt);
        alert('Error submitting data:\n' + response_txt);
      }
    } catch (error) {
      console.error('Error sending request:', error);
    }
  });