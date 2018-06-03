#!/usr/bin/python
from flask import Flask, render_template, request
from fair_bpm import file_dot_data_store
app = Flask(__name__)
store = file_dot_data_store()

@app.route('/')
def hello():
    mylist=store.list()
    return render_template('index.html', list=mylist)

@app.route("/show/<string:id>/", methods = ['GET', 'POST', 'DELETE'])
def show(id):
    ps=store.load(id)
    return render_template('show.html', id=id, ps=ps)

if __name__ == '__main__':
    print("Starting")
    app.run(debug=True)
