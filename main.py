import os, sys
from backorder.pipeline.training_pipeline import Training

from flask import Flask, render_template, request

application = Flask(__name__)

app = application

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5001, debug=True)