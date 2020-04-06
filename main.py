
from selenium import webdriver
import time
from flask import jsonify
import pandas as pd
import os, sys, csv, json
from auth import username, password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

        
def user_login(driver, username,password):

    delay = 10
    #driver.get("https://distilnetworks.com")
    driver.get("https://www.crunchbase.com/login")
    time.sleep(5)
    if driver.current_url == "https://www.crunchbase.com/login" or driver.current_url == "https://crunchbase.com/login":
        print(driver.current_url)
        login_user = 'mat-input-1'
        login_pass = 'mat-input-2'
        submit_class = 'button.mat-primary'
        
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, login_user)))

            print("Page is ready!")
            
        except TimeoutException:
            ActionChains(driver).click_and_hold(driver.find_element_by_css_selector('.px_captcha')).perform()
            print("Loading took too much time!")
             
        driver.find_element_by_id(login_user).send_keys(username)
        time.sleep(1);
        driver.find_element_by_id(login_pass).send_keys(password)
        time.sleep(1);

        driver.find_element_by_css_selector(submit_class).click();
        time.sleep(2)
    
    return driver

def JSON_to_CSV(json_file_path):
    dirname, json_file = os.path.split(os.path.abspath(json_file_path))
    csv_file = json_file.split(".")[0]+".csv"
    df = pd.read_json(json_file_path)
    df.to_csv (csv_file, index = None)
    csv_path = os.path.join(dirname, csv_file)
    return csv_path

    
def import_list(driver, file_pc):
    time.sleep(5)
    
    
    upload_class = 'div.right input'
    import_class = 'button.mat-accent'
    driver.get("https://www.crunchbase.com/csv-import");
    time.sleep(2);
    
    driver.execute_script("document.getElementsByTagName('input')[1].classList.remove('hide');");
    driver.execute_script("document.getElementsByTagName('input')[1].classList.remove('cb-hidden');");
    
    time.sleep(1);
    
    driver.find_element_by_css_selector(upload_class).send_keys(file_pc);
    time.sleep(3);
    driver.find_element_by_css_selector(import_class).click();
    #If main-message is visible
    #Let the list upload
    time.sleep(10)
    delay = 3
    #Wait until the file gets uploaded
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div .main-message')))
        
        print("Page view importedlist is ready!")

    except TimeoutException:
        ActionChains(driver).click_and_hold(driver.find_element_by_css_selector('iframe')).perform()
        print("Loading took too much time!")
    view_import_class = 'cta-button'
    driver.find_element_by_class_name(view_import_class).click()
    
    return driver

def select_download_list(driver):
    delay = 10
    #Wait until the page loads
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'component--results-info')))
        
        print("Page view Show Imported List is can be viewed now")

    except TimeoutException:
        print("Page view Show Imported List Loading took too much time!")
        
    #Click on columns to wait for facade
    driver.execute_script("var spanContainer; var spans = document.getElementsByTagName('span'); for (var i=0; i < spans.length; i++){ if (spans[i].innerHTML == 'Columns') { spanContainer = spans[i];}} spanContainer.click();")
    time.sleep(3)
    #Now wait for Check Dialog for Columns to open
    facade_class = 'component--dialog-layout'
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, facade_class)))
        
        print("Check Dialog for Columns can be viewed now")

    except TimeoutException:
        print("Check Dialog for Columns took too much time!")
    
    #Select All the from 5 - 12 mat-list-item-content
        driver.execute_script("var categs = document.getElementsByClassName('mat-list-item');"+
        "var checkboxes;"+
        "for (var i=5;i<=12;i++) {categs[i].click(); "+
        "                         checkboxes = document.getElementsByClassName('mat-checkbox-input');"+
        "                         for (var j=0;j<checkboxes.length;j++)"+
        "                         {"+
        "                             if (checkboxes[j].checked == false){"+
        "                                 checkboxes[j].click();}"+
        "                         } }"+
        "document.getElementsByClassName('mat-raised-button')[1].click();");
    time.sleep(1);
    driver.find_element_by_class_name('mat-raised-button').click();
    return driver

def download_file(driver):
    driver.execute_script("var spanContainer; var spans = document.getElementsByTagName('span'); for (var i=0; i < spans.length; i++){ if (spans[i].innerHTML == 'Export to CSV') { spanContainer = spans[i];}} spanContainer.click();")
    return driver;

def convert_output_json():
    dir_name, file_name = os.path.split(os.path.abspath(__file__))
    time.sleep(10)
    output_csv = os.path.join(os.path.join(dir_name, 'output'), os.listdir(os.path.join(dir_name, 'output'))[0])
    
    output_json = os.path.join(dir_name, 'output.json')
    
    csv_file = pd.DataFrame(pd.read_csv(output_csv, sep = ",", header = 0, index_col = False))
    
    csv_file.to_json(output_json, orient = "index", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)
    #remove the csv file after it is read and saved to json
    os.remove(output_csv)
    #df = pd.read_json(output_json)
    with open(output_json) as f:
        d = json.load(f)
        print(d)
        return jsonify(d)

def process(driver, json_file_path):

    driver_after_login = user_login(driver, username,password)
                                           
    csv_path = JSON_to_CSV(json_file_path)
                                           
    driver_after_import = import_list(driver_after_login,csv_path)

    driver_after_download_list =  select_download_list(driver_after_import)

    driver_after_download = download_file(driver_after_download_list)
    
    json_data = convert_output_json()
    #driver_after_download.close()
    return json_data, driver_after_download

#json_file_input = "E:\\UpWork\\2020\\April\\Crunch Base JSON to CSV\\input.json"
#process(json_file_input)
