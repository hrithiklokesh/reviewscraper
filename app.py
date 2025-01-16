from flask import Flask, jsonify, render_template, request
from scraper.scrape_reviews import scrape_reviews

app = Flask(__name__)

@app.route('/')
def home():
    """Serve the frontend page."""
    return render_template('index.html')

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    """API endpoint to scrape reviews."""
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        reviews = scrape_reviews(url)
        return jsonify({
            "reviews_count": len(reviews),
            "reviews": reviews
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
