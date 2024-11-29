import json
import random
import string
import firebase_admin
from firebase_admin import credentials, db

#Firebase here
cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://onlib-f4bf7-default-rtdb.firebaseio.com/"
})
    
ref_available_book = db.reference('AvailableBooks')

ref_users_data = db.reference('Users')

# "this function is to print list of books" 
def showAvailableBooks():
    data = ref_available_book.get()
    for bookid, bookinfo in data.items():
        print(f"{bookinfo['Title']} by {bookinfo['Author']} and id is {bookid}")
        
# "this function greet user"
def greetigs(name):
     print(f"Hello!{name} how are you?")
     showAvailableBooks()

#function that handel borrowing book
def borrowBook(name):
    bookUserWant = input("Which book do you want ? : ")
    bookFound = False
    data = ref_available_book.get()
    userData = ref_users_data.get()
    
    for bookid, bookinfo in data.items():
        if bookinfo['Title'] == bookUserWant:
            bookFound = True
            print(f"Thank you! you have to return {bookid} {bookinfo['Title']} in 30 days")
            
            randomUserId = random.randint(20,100)
            randomAge = random.randint(20,100)
            newUser = {
                f"user{randomUserId}":{
                    "name" : name,
                    "age" : randomAge
                }
            }
            ref_users_data.update(newUser)
            
            ref_available_book.child(f"{bookid}").delete()
            break
        
    if not bookFound:
        print(f"We do not have {bookUserWant} Sorry!")
        

# "this function is for retruning book"
def returnBook():
    bookUserReturn = input("Which book are you going to return ? : ")
    ref_all_book = db.reference('AllBookData')
    Alldata = ref_all_book.get()
    
    foundBook = False
    
    for bookid, bookinfo in Alldata.items():
        if bookinfo["Title"] == bookUserReturn:
            copiedValue = {bookid : bookinfo}
            ref_available_book.update(copiedValue)
            foundBook = True
            print("Thank you visit us again")
        
    if not foundBook:
        randomBookId = random.randint(600,1000)
        randomYear = random.randint(1900,2000)
        random_name = ''.join(random.choices(string.ascii_letters, k=8))
        newBook = {
            f"Book_{randomBookId}":{
                "Title" : bookUserReturn,
                "Author" : random_name,
                "Published Year" : randomYear
                }
            }
        print(newBook)
        ref_available_book.update(newBook)
        print("Thank you visit us again")
                    
# "main functon" 
def main():
    name = input(str("Your name is : "))
    greetigs(name)
    while True:
        try:
            userChoice = int(input("Which opreation will you perform ?\n1.Borrow books\n2.Return books\n3.Quit : "))
            if userChoice == 1:
                borrowBook(name)
            elif userChoice == 2:
                returnBook()
            elif userChoice == 3:
                print("Thank you visit again!")
                break
            else:
                print("Please type 1,2,3")
        except ValueError:
            print("Please type number only 1,2,3")


borrowBook("name")