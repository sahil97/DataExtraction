import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["dataextraction"]

mycol = mydb["keywords"]

initial = {
'Type': ['Industri', 'heltre', '1-stav', '2-stav', '3-stav', 'stavparkett', 'plank' , 'fiskebein', 'lamell', '1-lags',
            '2-lags', '3-lags', 'laminat', 'vinyl', 'vinylklikk'],
'Wood/Material': ['eik', 'ask', 'gran', 'furu', 'afrikansk eik', 'lønn', 'lerk', 'valnøtt', 'bøk'],
'sorting': ['rustik', 'natur', 'select', 'edel', 'sauvage', 'markant', 'exclusive', 'family', 'trend', 'favorit'],
'colour': ['full spectre'],
'subfloor': ['betong', 'sparkel', 'gips', 'spon', 'avrettingsmasse', 'GRANAB', 'Nivell', 'subfloor'],
'uderlay': ['plast', 'ullpapp', '2mm', '3mm', 'aquastop', 'silencio', 'etafoam', 'gips', 'lim'],
'others': ['priming', 'sliping', 'lakk', 'olje', 'behandlet', 'ubehandlet', 'børstet', 'strukturert']
}


x = mycol.insert_one(initial)

print("Inserted into db")
