def form_sentence(df):
    temp_sentence = ''
    for i in range(len(df.values)):
        if( i != 0):
            temp_sentence += ', ' + df.values[i][0]
        else:
            temp_sentence += df.values[i][0]
    return temp_sentence

def form_dates_time(df):
    date_time_list = []
    date_time_list.append(
        {
            df.keys()[0] : df.keys()[1]
        }
    )
    for key,value in df.values:
        date_time_list.append(
            {
                key : value
            }
        )
    return date_time_list

def extract_from_keywords(df):
    keywords = ['Weight', 'Loadmeter', 'Goods']
    return_list = []
    for row in df.values.tolist():
        for keyword in keywords:
            if keyword in str(row[0]):
                try:
                    return_list.append({
                       row[0].split(':')[0] : row[0].split(':')[1]
                    })
                except Exception as e:
                    continue
    return return_list

def extract_goods_list(df):
    temp_df = df.copy()
    temp_df['Product'] = temp_df['Unnamed: 1']
    temp_df.drop(['Unnamed: 1'], axis=1, inplace=True)
    return temp_df.to_dict(orient='records')[0]
