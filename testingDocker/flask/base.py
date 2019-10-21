import os
import time
from werkzeug.utils import secure_filename
import numpy as np
import pandas as pd
import json
import tabula
import math
from flask import jsonify
import img_proc as img_proc


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

#     templates = {
#         'page1': (204.91, 33.138, 811.816, 570.86),
#         'page2': (107.49, 36.113, 800.672, 563.43)
#     }
    pages = 6
    default_columns = ['Post', 'Beskrivelse', 'Enh.', 'Mengde', 'Enhetspris', 'Sum']
    area_temp = img_proc.extract_cords_from_pdf(new_filename)
    word_list = [
    'Type','Wood','material','sorting','colour', 'subfloor', 'underlay', 'others', 'Industri', 'eik',
    'rustik', 'full spectre', 'betong', 'plast', 'priming', 'heltre', 'ask', 'natur', 'sparkel', 'ullpapp',
    'sliping', '1-stav', 'lønn', 'select', 'gips', '2mm', 'lakk', '2-stav', 'lerk', 'edel', 'spon', '3mm', 'olje',
    '3-stav', 'valnøtt', 'sauvage', 'avrettingsmasse', 'aquastop', 'behandlet', 'stavparkett', 'bøk',
    'markant', 'GRANAB', 'silencio', 'dim', '6-36mm', 'ubehandlet', 'plank', 'afrikansk eik','exclusive',
    'Nivell',' etafoam', 'børstet', 'fiskebein', 'furu', 'family', 'subfloor', 'gips', 'strukturert', 'lamell',
    'gran', 'trend', 'lim', '1-lags','favorit', '2-lags', '3-lags', 'laminat', 'vinyl', 'vinylklikk'
]

    df_final = pd.DataFrame(columns = default_columns)

    for i in range(1, len(area_temp)):
        if(i == 1):
            df = tabula.read_pdf(new_filename, pages='1', area=area_temp[i-1])
            for col in df.columns:
                if((df[col].isnull().sum()/len(df))>0.98 and col=='Post'):
                    df.drop([col], axis=1, inplace=True)

            try:
                df.columns = default_columns
            except ValueError as e:
                for col in default_columns:
                    if(col not in df.columns):
                        if(col == 'Enhetspris' or col == 'Sum'):
                            df[col] = ""
                        else:
                            continue
            df.columns = default_columns
            # Error correction for column names
    #         df['Post'] = df['Unnamed: 0']
    #         df.drop(['Unnamed: 0'], axis=1, inplace=True)

    #         df['Sum'] = df['Unnamed: 7']
    #         df.drop(['Unnamed: 7'], axis=1, inplace=True)

            df_final_temp = extract_columns(df)
            df_final = pd.concat([df_final, df_final_temp])


        elif(i > 1):
            df = tabula.read_pdf(new_filename, pages=i, area=area_temp[i-1])
            for col in df.columns:
                if('Sum' in list(df[col])):
                    df.drop([col], axis=1, inplace=True)
                elif((df[col].isnull().sum()/len(df))>0.98):
                    df.drop([col], axis=1, inplace=True)


            try:
                df.columns = default_columns
            except ValueError as e:
                for col in default_columns:
                    if(col not in df.columns):
                        if(col == 'Enhetspris' or col == 'Sum'):
                            df[col] = ""
                        else:
                            continue
            df.columns = default_columns
            df_final_temp = extract_columns(df)
            df_final = pd.concat([df_final, df_final_temp])
    df_final = df_final.reset_index()
    for index, rows in df_final.iterrows():
        drop = 1
        for word in list(rows['Beskrivelse'].split(' ')):
            if word in word_list:
                drop = 0
        if(rows['Post'] == 'Post'):
            drop = 1
        if(drop != 0):
            df_final.drop([index], axis=0, inplace=True)
    df_final.drop(['index'], axis=1, inplace=True)

    return df_final


def extract_columns(df):
    sorted_indexes = handle_sort(df)

    df_new = get_new_df(df, sorted_indexes)

    return df_new

def handle_sort(df):
    # Correction for Sorting
    for post in df['Post'].value_counts().keys():
        if(len(post.split('.')) < 4 and post != 'Post'):
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
                sentence_list[i].append(str(df[df.columns[1]][j]) + " \n")

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
                sentence_list[i].append(str(df[df.columns[1]][j]) + " \n")

                for k in range(2, len(df.columns)):
                    if(type(df[df.columns[k]][j]) == str):
                        list_dict[df.columns[k]][i] = df[df.columns[k]][j]

            sentence_list[i] = " ".join(sentence_list[i])


    df_new[df.columns[1]] = sentence_list
    for k in range(2, len(df.columns)):
            df_new[df.columns[k]] = list_dict[df.columns[k]]

    return df_new
