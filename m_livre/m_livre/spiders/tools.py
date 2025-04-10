# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:47:14 2024

@author: Mucho
"""

from .settings import db_path
from urllib.parse import urlencode

def save_pkl(obj, name='object', path=db_path):
    import pickle
    file_path = f'{path}/{name}.pkl'
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)
        file.close()

def load_pkl(name='object', path=db_path):
    import pickle
    file_path = f'{path}/{name}.pkl'
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        file.close()
    return data

def url_encoded(base:str,query:str)->str:
    search_query = query
    params = {"q": search_query}
    encoded_params = urlencode(params)

    url = f"{base}?{encoded_params}"
    return url