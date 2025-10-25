# данная функция для прохождения по дереву и сбору всех итерируемых
# полей в один "плоский" список
from collections.abc import Iterable

def flatten(*itarebles, flat_list=None):
    if flat_list is None:
        flat_list = []
    
    for item in itarebles:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            flatten(*item, flat_list=flat_list)
        else:
            flat_list.append(item)
    
    return flat_list

DATA = [1, [2, [3, [4, 5]]]]

print(flatten(DATA))
# [1, 2, 3, 4, 5]
