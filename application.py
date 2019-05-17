from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    if tweets==None:
        return redirect(url_for("index"))

    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    analyzer = Analyzer(positives, negatives)
    
    positive, negative, neutral, s = 0.0, 0.0, 0.0, 0.0
    
    for tweet in tweets:
        score=analyzer.analyze(tweet)
        if score>0:
            positive+=1
        elif score<0:
            negative+=1
        else:
            neutral+=1
            
    s=positive+negative+neutral
    
    try:
        positive=(positive/s)*100
    except:
        positive=0
    
    try:
        negative=(negative/s)*100
    except:
        negative=0
    
    try:
        neutral=(neutral/s)*100
    except:
        neutral=0
        
    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)

if __name__ == '__main__':
    app.run(debug=True)
