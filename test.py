import pandas as pd
import json
 
with open("tmp/azure_extraction.json","r") as obj:
    data=json.load(obj)
    df=pd.DataFrame