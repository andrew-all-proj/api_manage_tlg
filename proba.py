
id_telegram = None





def foo(id):
    if (not id): return id
    return "".join(str(id).split()) or id


print(foo("159959592\n  "))