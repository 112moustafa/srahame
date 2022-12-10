
from flask import Flask


PORT = 5000


app = Flask(__name__)



###############

@app.route('/' )
def index():
    return "hh"
#########################


#########################################################to run the website####################################################################
if __name__ == "__main__":
    app.run(debug=True, port=PORT, host='0.0.0.0')
