from flask import Flask, request
import pandas as pd
import os

app = Flask(__name__)

# Load Excel file
df = pd.read_csv("complaints.csv")

@app.route("/api/search", methods=["GET"])
def search_complaints():
    keyword = request.args.get("keyword")

    if not keyword:
        return "<h3>Error: keyword parameter is required</h3>"

    # Filter rows where Review contains keyword
    results = df[df["Review"].str.contains(keyword, case=False, na=False)]

    # Select only required columns
    selected = results[["Last Name", "First Name", "Review"]]

    # Convert to HTML table
    table_html = selected.to_html(index=False)

    # Return a simple webpage
    return f"""
    <html>
        <head>
            <title>Search Results</title>
        </head>
        <body>
            <h2>Results for keyword: "{keyword}"</h2>
            {table_html}
        </body>
    </html>
    """
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)