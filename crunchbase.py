from main import *
import os
import json
import undetected_chromedriver


from flask import Flask, request

#DEBUG=os.environ["DEBUG_LINKEDIN_ENDPOINT"]=="True"

app = Flask(__name__)
app.driver = None
@app.route("/get_company_details", methods=["POST"])
def json_to_file():
    if (app.driver == None):
        undetected_chromedriver.install()
        dir_name, file_name = os.path.split(os.path.abspath(__file__))
        print(dir_name, file_name)
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : os.path.join(dir_name, 'output')}
        chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation']);
        chromeOptions.add_experimental_option("prefs",prefs)
        chromeOptions.add_argument("user-data-dir=selenium1")
        #chromeOptions.add_argument("--incognito")
        chromedriver = "chromedriver.exe"
        app.driver = webdriver.Chrome(chrome_options=chromeOptions)
    #Write the input file to JSON
    data = json.loads(request.data)
    dir_name, file_name = os.path.split(os.path.abspath(__file__))
    json_input_path = os.path.join(dir_name, 'input.json')
    with open(json_input_path, 'w') as outfile:
        json.dump(data, outfile)
    
    #json_input_path = the file where json is written
    #json_file_path = "E:\\UpWork\\2020\\April\\Crunch Base JSON to CSV\\input.json"

    output_json, app.driver = process(app.driver, json_input_path)
    
    return output_json


app.run(host="localhost")
