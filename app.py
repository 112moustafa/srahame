
from flask import Flask, render_template, redirect, session, request, flash



PORT = 5000


app = Flask(__name__)




# create flask app
app, db = create_app()

####################


###############

@app.route('/' )
def index():
    return "hh"
#########################


#########################################################to run the website####################################################################
if __name__ == "__main__":
    app.run(debug=True, port=PORT, host='0.0.0.0')
