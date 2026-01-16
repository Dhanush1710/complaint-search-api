from flask import Flask, request
import pandas as pd
import os

app = Flask(__name__)

# Load CSV
df = pd.read_csv("complaints.csv")

# Homepage UI
@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Complaint Search</title>
        </head>
        <body style="font-family: Arial; padding: 40px;">
            <h2>Complaint Search Tool</h2>

            <form action="/api/search" method="get">
                <input 
                    type="text" 
                    name="keyword" 
                    placeholder="Enter keyword (e.g., good, bad, service)" 
                    style="padding:10px; width:300px;"
                    required
                />
                <button style="padding:10px;">Search</button>
            </form>
        </body>
    </html>
    """

# Search endpoint
@app.route("/api/search", methods=["GET"])
def search_complaints():
    keyword = request.args.get("keyword")

    if not keyword:
        return "<h3>Error: keyword parameter is required</h3>"

    results = df[df["Review"].str.contains(keyword, case=False, na=False)]

    selected = results[["Business", "Experience", "Last Name", "First Name", "Review"]]

    table_html = selected.to_html(index=False)

    return f"""
    <html>
        <head>
            <title>Results</title>
        </head>
        <body style="font-family: Arial; padding: 40px;">
            <h2>Results for keyword: "{keyword}"</h2>

            <a href="/">← Back to Search</a><br><br>

            {table_html}
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
