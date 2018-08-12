def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

valid_object = {
    "name": "F",
    "price": 6.99,
    "isbn": 2123435455
}

missing_name = {
    "price": 6.99,
    "isbn": 2123435455
}

missing_price = {
    "name": "F",
    "isbn": 2123435455
}

for i in [valid_object, missing_name, missing_price]:
    print(validBookObject(i))