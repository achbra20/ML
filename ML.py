from flask import Flask
from classe import Destination, Boats
from flask import jsonify
from flask import request

app = Flask(__name__)

url = "http://www.awesome.test/Api_ml/all_request"
urlcrm ="http://www.awesome.test/Api_ml/all_demande"

@app.route('/<country>')
def distination_top(country):
    distination = Destination()
    new_list= distination.top_crm_win_destination(url,urlcrm,country)
    return jsonify(new_list)

@app.route('/boat/<country>')
def boats_top(country):
    boats = Boats()
    new_list= boats.top_10_yacht(country,url)
    return jsonify(new_list)

@app.route('/boat_des')
def boats_des_top():
    destination = request.args['destination']
    country = request.args['country']
    boats = Boats()
    new_list= boats.top_10_yacht_destination(url,country,destination)
    return jsonify(new_list)

@app.route('/boat_type')
def boats_top_type():
    boats = Boats()
    new_list= boats.top_10_yacht_type(url)
    return jsonify(new_list)

if __name__ == '__main__':
    app.run(debug= True)
