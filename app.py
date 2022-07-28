from flask import Flask
from premium.logger import logging
from  premium import exception
import sys
app=Flask(__name__)


@app.route("/",methods=['GET','POST'])
def index():
    #try:
        #raise Exception("We are testing custom exception")
    #except Exception as e:
        #premium = exception.HousingException(e,sys)
        #logging.info(premium.error_message)
        #logging.info("We are testing logging module")
    return "Starting MAchine Learning Project"


if __name__=="__main__":
    app.run(debug=True)
