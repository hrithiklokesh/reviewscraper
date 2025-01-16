# reviewscraper
# Review Scraper API

This project is a web-based review scraper that fetches reviews from product pages. It identifies review elements dynamically using OpenAI's GPT-3.5-turbo and Playwright for browser automation. The API provides scraped review data at the `/api/reviews` endpoint.

---

## Features

- Scrape product reviews dynamically.
- Automatically identify review elements (title, body, rating, and reviewer) using an AI model.
- Load all reviews, including paginated content.
- Simple HTML interface for users to input URLs.
- API endpoint (`/api/reviews`) for programmatic access.

---

## File Structure

project/ │ ├── app.py # Main entry point for the Flask app ├── requirements.txt # Python dependencies ├── README.md # Project documentation │ ├── scraper/ # Scraper logic folder │ ├── init.py # Package initialization (optional) │ ├── scrape_reviews.py # Scraper functions and logic │ ├── utils.py # Utility functions │ ├── templates/ # HTML templates for the UI │ └── index.html # Main HTML form for URL input │ ├── static/ # Static files (CSS, JavaScript) │ ├── css/ │ │ └── styles.css # Styling for the HTML interface │ ├── js/ │ │ └── script.js # JavaScript for form submission and rendering │ └── tests/ # Test files (optional) └── test_scraper.py # Unit tests for scraper functions

## Set up a virtual environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

## Install dependencies

pip install -r requirements.txt

## Start the Flask server

python app.py

## Open the application in your browser
Navigate to http://127.0.0.1:5000.

## Input the URL
Enter the URL of the product page you want to scrape and click Scrape Reviews.

## API Endpoint
/api/reviews

## Contributing
Contributions are welcome! Please open an issue or submit a pull request with your suggestions.
