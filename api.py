from flask import Flask, request
import pandas as pd
import os

app = Flask(__name__)

#reading the csv file
df = pd.read_csv("complaints.csv")

#home page
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Complaint Search</title>
    </head>

    <body style="font-family: Arial; padding: 30px;">

        <h2>Search Complaints</h2>

        <p>Type a keyword to search in complaints</p>

        <form action="/api/search" method="get">

            <input type="text" name="keyword" 
                placeholder="type something like bad, service, slow" 
                style="padding:8px; width:280px;" required>

            <br><br>

            <button style="padding:8px;">Search</button>

        </form>

    </body>
    </html>
    """

#api for searching complaints
@app.route("/api/search")
def search_complaints():

    keyword = request.args.get("keyword")

    if keyword == None or keyword == "":
        return "<h3>Please enter a keyword</h3>"

    #filter rows where review contains the keyword
    results = df[df["Review"].str.contains(keyword, case=False, na=False)]

    selected = results[["Business", "Experience", "Last Name", "First Name", "Review"]]

    table_html = selected.to_html(index=False)

    return f"""
    <html>
    <head>
        <title>Search Result</title>
    </head>

    <body style="font-family: Arial; padding: 30px;">

        <h2>Results for: {keyword}</h2>

        <a href="/">Go Back</a>

        <br><br>

        {table_html}

    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

