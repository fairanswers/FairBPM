#!/usr/bin/python
from flask import Flask, render_template, request
from fair_bpm import file_dot_data_store, Process, create_runner
app = Flask(__name__)
store = file_dot_data_store()
runner = create_runner()

@app.route('/')
def index():
    mylist=store.list()
    return render_template('index.html', list=mylist)

@app.route('/delete/<string:id>/', methods = ['DELETE'])
def dot_delete(id):
    store.delete(id)
    return "Deleted."

@app.route("/show/<string:id>/", methods = ['GET', 'POST', 'DELETE'])
def show(id):
    ps=store.load(id)
    return render_template('show.html', id=id, ps=ps)

@app.route("/save/<string:id>/", methods = ['GET', 'POST', 'DELETE'])
def save(id):
    file = request.data
    ps = Process.parse(file)
    store.save(ps)
    return ps.to_dot()

@app.route("/run/", methods = ['POST'])
def run():
    file = request.data
    ps = Process.parse(file)
    result=runner.run(ps)
    return result.to_dot()

if __name__ == '__main__':
    print("Starting")
    app.run(debug=True)
