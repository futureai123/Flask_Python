from flask import Flask, jsonify, request, Response, json
import json
from settings import *
#code to be revied
#code is a sample

# moved to settings.py app = Flask(__name__)

books = [
    {'name': 'A',
     'price': '7,99',
     'isbn': 1234561290
     },
    {'name': 'B',
     'price': '6.99',
     'isbn': 4243252345
     }
]


@app.route('/books')
def host_app():
    return jsonify({'books': books})


# POST /books
# {
#    'name': 'F',
#    'price' 6.99,
#    'isbn': 0123435455
# }

"""Sanitazing """


def validBookObject(bookObject):
    if "name" in bookObject and "price" in bookObject and "isbn" in bookObject:
        return True
    else:
        return False


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    """sanitazing by request content structure"""
    if validBookObject(request_data):
        """sanitazing data by excluding no_valid keys"""
        new_book ={
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Use json schema {'name': 'bookname', 'price': 7.76, 'isbn': 9876575432"
            }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }
            return jsonify(return_value)

#Put Request
#{
#	"name": "The Odyssey",
#	"price": "6.99"
#}

def valid_put_request_data(bookObject):
    if "name" in bookObject and "price" in bookObject:
        return True
    else:
        return False

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Use json schema {'name': 'bookname', 'price': 7.76"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    new_book = {
        "name": request_data['name'],
        "price": request_data['price'],
        "isbn": isbn
    }
    i=0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
            books.pop(i)
        i += 1
    "no content response is standard that update was succesfull"
    response = Response("", status=204)

    return response

#PATCH
#{
#    "name": "Harry Potter and the Chaber of the Secrets"
#}

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if "name" in request_data:
        updated_book["name"] = request_data['name']
    elif "price" in request_data:
        updated_book["price"] = request_data['price']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


# DELETE /books/4243252345
@app.route('/books/<int:isbn>', methods={'DELETE'})
def delete_book(isbn):
    #request.get_json() In this case request body is not a case
    #it is something like: for idx, val in enumerate(<dict>)
    i = 0;
    for book in books:
        if book["isbn"] in books:
            book.pop(i)
            response = Response("", status=204, mimetype='application/json')
            return response
        i == 1

    invalidBookObjectErrorMsg = {
        "error": "Request subject not found"
    }

    response = Response(invalidBookObjectErrorMsg, status=404, mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run()
