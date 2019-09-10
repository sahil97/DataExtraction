import os
import time
from werkzeug.utils import secure_filename
import numpy as np
import pandas as pd
import json
import tabula
import math
from flask import jsonify


def init(file):

    # Getting filename for saving the processed file with the same name
    filename = secure_filename(file.filename)
    print(filename)

    try:
        file.save(filename)
        print("file saved")
    except Exception as e:
        print(e)

    try:
        result_df = extract_data(filename)
        print("got the new DF")
    except Exception as e:
        print(e)

    return jsonify({"Message" : "File uploaded successfully",
                    "Result" : result_df.to_dict(orient="records")}), 200



def extract_data(new_filename):

    # Hardcoded stuff for now

    templates = {
        'page1': (204.91, 33.138, 811.816, 570.86),
        'page2': (107.49, 36.113, 800.672, 563.43)
    }
    pages = 6
    default_columns = ['Post', 'Beskrivelse', 'Enh.', 'Mengde', 'Enhetspris', 'Sum']

    df_final = pd.DataFrame(columns = default_columns)

    for i in range(1, pages):

        if(i == 1):
            df = tabula.read_pdf('MyExport.pdf', pages='1', area=templates['page1'])

            # Error correction for column names
            df['Post'] = df['Unnamed: 0']
            df.drop(['Unnamed: 0'], axis=1, inplace=True)

            df['Sum'] = df['Unnamed: 7']
            df.drop(['Unnamed: 7'], axis=1, inplace=True)

            df_final_temp = extract_columns(df)
            df_final = pd.concat([df_final, df_final_temp])

        elif(i > 1):
            print(i)
            df = tabula.read_pdf('MyExport.pdf', pages=i, area=templates['page1'])
            df.columns = default_columns

            df_final_temp = extract_columns(df)

            df_final = pd.concat([df_final, df_final_temp])

    return df_final


def extract_columns(df):
    sorted_indexes = handle_sort(df)

    df_new = get_new_df(df, sorted_indexes)

    return df_new

def handle_sort(df):
    # Correction for Sorting
    for post in df['Post'].value_counts().keys():
        if(len(post.split('.')) < 4):
            df['Post'][df.index[df['Post'] == post][0]] += '.00'

    sorted_indexes = list(df['Post'].value_counts().keys())
    sorted_indexes.sort()
    return sorted_indexes

def get_new_df(df, sorted_indexes):


    # Making the dataframe index_wise

    df_new = pd.DataFrame()
    df_new[df.columns[0]] = list(sorted_indexes)


    # Variables for holding temp values that will be later assigned to the dataFrame

    sentence_list = []
    list_dict = {}

    for i in range(2, len(df.columns)):
        list_dict[df.columns[i]] = []


    # Traversing through the read file from tabula
    for i in range(len(sorted_indexes)):

        sentence_list.append([])

        for k in range(2, len(df.columns)):
            list_dict[df.columns[k]].append(' ')

    # For the first n-1 lines
        if(i+1 < len(sorted_indexes)):

    # Getting all rows between 2 consecutive indexes such as (12.0.1, 12.0.1.01) etc.
            i1 = df.index[df['Post'] == sorted_indexes[i]][0]
            i2 = df.index[df['Post'] == sorted_indexes[i+1]][0]

            for j in range(i1, i2):

    # Adding a new line after
                sentence_list[i].append(df[df.columns[1]][j] + " \n")

    # Handling rest of the value columns
                for k in range(2, len(df.columns)):
                    if(type(df[df.columns[k]][j]) == str):
                        list_dict[df.columns[k]][i] = df[df.columns[k]][j]

            sentence_list[i] = " ".join(sentence_list[i])

    # For the last line
        elif(i+1 >= len(sorted_indexes)):

            i1 = df.index[df['Post'] == sorted_indexes[i]][0]
            i2 = len(df)

            for j in range(i1, i2):

    # Adding a new line after
                sentence_list[i].append(df[df.columns[1]][j] + " \n")

                for k in range(2, len(df.columns)):
                    if(type(df[df.columns[k]][j]) == str):
                        list_dict[df.columns[k]][i] = df[df.columns[k]][j]

            sentence_list[i] = " ".join(sentence_list[i])


    df_new[df.columns[1]] = sentence_list
    for k in range(2, len(df.columns)):
            df_new[df.columns[k]] = list_dict[df.columns[k]]

    return df_new
