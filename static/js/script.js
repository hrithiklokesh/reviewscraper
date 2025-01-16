document.getElementById('scraper-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    const urlInput = document.getElementById('url').value.trim();
    const resultsContainer = document.getElementById('results');

    // Clear previous results
    resultsContainer.innerHTML = '';

    if (!urlInput) {
        resultsContainer.innerHTML = '<p class="error">Please enter a valid URL.</p>';
        return;
    }

    try {
        // Send the URL to the API endpoint
        const response = await fetch('/api/reviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: urlInput }),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        // Parse the JSON response
        const data = await response.json();

        if (data.success) {
            resultsContainer.innerHTML = `<h2>Found ${data.reviews_count} Reviews</h2>`;
            data.reviews.forEach((review, index) => {
                const reviewHtml = `
                    <div class="review">
                        <h3>Review ${index + 1}</h3>
                        <p><strong>Title:</strong> ${review.title}</p>
                        <p><strong>Body:</strong> ${review.body}</p>
                        <p><strong>Rating:</strong> ${review.rating}</p>
                        <p><strong>Reviewer:</strong> ${review.reviewer}</p>
                    </div>
                `;
                resultsContainer.innerHTML += reviewHtml;
            });
        } else {
            resultsContainer.innerHTML = `<p class="error">Failed to scrape reviews: ${data.error}</p>`;
        }
    } catch (error) {
        resultsContainer.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
});
