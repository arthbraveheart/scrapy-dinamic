# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:47:14 2024

@author: Mucho
"""

from settings import db_path


def save_pkl(obj, name='object', path=db_path):
    import pickle
    file_path = path + name + '.pkl'
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)
        file.close()

def load_pkl(name='object', path=db_path):
    import pickle
    file_path = path + name + '.pkl'
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        file.close()
    return data