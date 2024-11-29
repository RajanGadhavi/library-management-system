import json
import firebase_admin
from firebase_admin import credentials, db, firestore 

#Firebase here
cred = credentials.Certificate("cred.json") 
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://onlib-f4bf7-default-rtdb.firebaseio.com/"
})

#Books data stored on local storge to firebase 
bookFilePath = r"D:\Data\Python\New Begging\library-management-system\booksData.json"
with open(bookFilePath, "r") as file:
    books_dict = json.load(file)
    
#User data stored on local storge to firebase
userFilePath = r"D:\Data\Python\New Begging\library-management-system\userData.json"
with open(userFilePath, "r") as file:
    user_dict = json.load(file)

#pushing All book data
refToAllBook = db.reference('AllBookData')
refToAllBook.set(books_dict)

#pushing avalaible book data
refToAvalaibleBook = db.reference('AvailableBooks')
refToAvalaibleBook.set(books_dict)

#pushing users data
refToUser = db.reference('Users')
refToUser.set(user_dict)
