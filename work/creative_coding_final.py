# To use this module, put the .py file in the same directory as your notebook
# 
# from creative_coding_final import *
#

import csv
from datetime import datetime
from google import genai
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

def get_data_from_csv(file_name, columns_list=[]):
    
    print("Note: Your data will be returned as a list of dictionaries where all keys and values are strings")
    
    if not file_name.endswith(".csv"):
        print("Error: file_name must end with .csv")
        return

    with open(file_name, newline="") as csvfile:
        
        reader = csv.DictReader(csvfile)
        
        if not columns_list:
            print("columns_list is not specified. Keeping all columns...")
            data = list(reader)
        else:
            print("Using only columns ", columns_list)
            columns_only = lambda x: {k: x[k] for k in columns_list if k in x}
            data = [columns_only(row) for row in reader]

    print(f"There are {len(data)} rows of data")
    print(f"The first row is \n\n{data[0]}")
    
    return data

        
def convert_dates(data, key, date_formats=["%Y-%m-%d", "%Y"]):

    print(f"Converting all the values for the key {key} into dates")
    print(f"Using date_formats: {date_formats}... Will try each one in order until one works")

    for date_format in date_formats:
        try:
            datetime.now().strftime(date_format)
        except ValueError:
            print(f"Error: date_format is invalid: {date_format}")
            print("date_format should be something like %Y-%m-%d")
            print("See https://www.w3schools.com/python/gloss_python_date_format_codes.asp for help")
            return 

    n = len(data)
    new_keys = set()
    for i in range(n):
        for df in date_formats:
            try:
                result = datetime.strptime(data[i][key], date_formats[0])
                break
            except:
                continue
        if not result:
            print(f"Unable to parse row the value in row {i}: {data[i][key]}")
            
        new_dict = parse_datetime_object(result, key, df)
        for k in new_dict:
            new_keys.add(k)
        data[i].update(new_dict)

    print(f"New keys added: {new_keys}")
    print("Success. Returning data...")
    return data


def parse_datetime_object(parsed_date, prefix, format_string):
    
    supported_letters = "YymdHMSbB%-/"   
    unsupported_codes = []
    for letter in format_string:
        if letter not in supported_letters:
            unsupported_codes.append(letter)
            
    if unsupported_codes:
        print(f"Warning: Unsupported format codes detected: {', '.join(unsupported_codes)}")
        print("Contact Sarah if you need anything besides year, month, day, hour, minute, or second")
   
    components = {}

    if "%Y" in format_string or "%y" in format_string:
        components[f"{prefix}_year"] = parsed_date.year
    if "%m" in format_string or "%b" in format_string or "%B" in format_string:
        components[f"{prefix}_month"] = parsed_date.month
    if "%d" in format_string:
        components[f"{prefix}_day"] = parsed_date.day
    if "%H" in format_string:
        components[f"{prefix}_hour"] = parsed_date.hour
    if "%M" in format_string:
        components[f"{prefix}_minute"] = parsed_date.minute
    if "%S" in format_string:
        components[f"{prefix}_second"] = parsed_date.second

    return components


def convert_numbers(data, key):

    print(f"Converting values for key {key} to floats...")
    n = len(data)
    for i in range(n):
        data[i][f"{key}_float"] = float(data[i][key])
    print(f"Done. New key added: '{key}_float'")
    return data


def start_gemini(gemini_key):
    client = genai.Client(api_key=gemini_key)
    return client


def ask_gemini(client, prompt):
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text


def sort_by_value(counts_dict):
    return sorted(counts_dict.items(), key=lambda item: item[1], reverse=True)
    
    

    
    



    
