# Filename - server.py
 
# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify
from cv_to_profile import cvToProfile
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


     
# Running app
if __name__ == '__main__':
    app.run(debug=True)