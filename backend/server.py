# Filename - server.py
 
# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify
from cv_to_profile import cvToProfile

from stage_1 import getIndustries
from stage_2 import getJobs
from stage_3 import getSpecialisations
from final import getSummary
import datetime
 
x = datetime.datetime.now()
 
# Initializing flask app
app = Flask(__name__)
 
 
# Route for seeing a data
@app.route('/data', methods=['POST'])
def parseCV():
    data = request.get_json()
    cv_text = data.get('cv_text')
    # Returning an api for showing in reactjs
    return cvToProfile(cv_text)


@app.route('/stage1', methods=['POST'])
def getStage1Buttons():
    data = request.get_json()
    #print("printing data")
    #print(data)
    # cv_text = data.get('cv_text')
    # Returning an api for showing in reactjs
    return getIndustries(data)

@app.route('/stage2', methods=['POST'])
def getStage2Buttons():
    data = request.get_json()
    profile = data.get("profile")
    msg = data.get("message")
    #print("printing data")
    #print(data)
    # cv_text = data.get('cv_text')
    # Returning an api for showing in reactjs
    return getJobs(profile,msg)

@app.route('/stage3', methods=['POST'])
def getStage3Buttons():
    data = request.get_json()
    profile = data.get("profile")
    msg1 = data.get("message1")
    msg2 = data.get("message2")

    #print("printing data")
    #print(data)
    # cv_text = data.get('cv_text')
    # Returning an api for showing in reactjs
    return getSpecialisations(profile,msg1,msg2)

@app.route('/final', methods=['POST'])
def final():
    data = request.get_json()
    profile = data.get("profile")
    msg = data.get("message")

    #print("printing data")
    #print(data)
    # cv_text = data.get('cv_text')
    # Returning an api for showing in reactjs
    return getSummary(profile,msg)
     
# Running app
if __name__ == '__main__':
    app.run(debug=True)