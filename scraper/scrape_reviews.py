from playwright.sync_api import sync_playwright, TimeoutError
import openai
import os
import time

# Load OpenAI API key from environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
else:
    print("Warning: OPENAI_API_KEY not set. LLM-based CSS identification won't work.")

def identify_review_selectors(html_content):
    """Use an LLM to identify dynamic CSS selectors for reviews."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required for dynamic CSS identification.")

    prompt = f"Given the following HTML content, identify the CSS selectors for reviews, including title, body, rating, and reviewer:\n\n{html_content}\n\nProvide the result as a JSON object with keys 'title', 'body', 'rating', 'reviewer'."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        selectors = response['choices'][0]['message']['content'].strip()
        return eval(selectors)  # Assumes LLM returns a valid JSON-like structure
    except Exception as e:
        raise RuntimeError(f"Failed to query OpenAI API or parse selectors: {e}")

def extract_reviews_from_page(page, selectors):
    """Extract reviews from a single page based on the provided CSS selectors."""
    reviews = []
    try:
        titles = page.query_selector_all(selectors.get('title', 'h3'))
        bodies = page.query_selector_all(selectors.get('body', '.review-text'))
        ratings = page.query_selector_all(selectors.get('rating', '.review-rating'))
        reviewers = page.query_selector_all(selectors.get('reviewer', '.review-author'))

        for title, body, rating, reviewer in zip(titles, bodies, ratings, reviewers):
            reviews.append({
                "title": title.text_content().strip() if title else "No Title",
                "body": body.text_content().strip() if body else "No Body",
                "rating": int(rating.text_content().strip()[0]) if rating else 0,
                "reviewer": reviewer.text_content().strip() if reviewer else "Anonymous"
            })
    except Exception as e:
        raise RuntimeError(f"Failed to extract reviews: {e}")

    return reviews

def scroll_to_load(page):
    """Simulate scrolling to load all reviews."""
    previous_height = 0
    while True:
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)  # Wait for loading
        current_height = page.evaluate('document.body.scrollHeight')
        if current_height == previous_height:
            break
        previous_height = current_height

def scrape_reviews(url):
    """Main function to scrape reviews from the provided URL."""
    if not url:
        raise ValueError("URL parameter is required.")

    reviews = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.set_default_timeout(60000)  # Increase timeout to 60 seconds
            page.goto(url)

            # Load all reviews dynamically
            scroll_to_load(page)

            # Get page content and use LLM to identify selectors
            html_content = page.content()
            selectors = identify_review_selectors(html_content)

            # Extract reviews
            while True:
                reviews.extend(extract_reviews_from_page(page, selectors))

                # Check for a "Next" button and navigate if present
                try:
                    next_button = page.query_selector('a.next')  # Adjust as needed
                    if next_button and next_button.is_enabled():
                        next_button.click()
                        page.wait_for_load_state('networkidle')
                    else:
                        break
                except TimeoutError:
                    print("Next button not found or page timed out.")
                    break

        except Exception as e:
            raise RuntimeError(f"An error occurred during scraping: {e}")
        finally:
            browser.close()

    return reviews

# Function to integrate with other components or APIs
def scrape_reviews_api(url):
    """API-friendly function to scrape reviews."""
    try:
        reviews = scrape_reviews(url)
        return {
            "success": True,
            "reviews_count": len(reviews),
            "reviews": reviews
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
