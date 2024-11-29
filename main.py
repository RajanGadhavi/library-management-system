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
ref_users_data = db.reference('Users/UsersData')

# "this function is to print list of books" 
def showAvailableBooks():
    data = ref_available_book.get()
    for bookid, bookinfo in data['BookData'].items():
        print(f"{bookinfo['Title']} by {bookinfo['Author']}")
        
# "Add new user"
def addNewUser(name, bookUserWant):
    randomUserId = random.randint(20,100)
    randomAge = random.randint(20,100)
    newUser = {
        f"user{randomUserId}":{
                "name" : name,
                "age" : randomAge,
                "book" : bookUserWant
            }
        }
    ref_users_data.update(newUser)
    
#"This function will update user data when user borrow book"     
def userBorrowBook(name,bookUserWant):
    usersData = ref_users_data.get()
    for userId, userInfo in usersData.items():
        if userInfo['name'] == name:
            userRef = db.reference(f'Users/UsersData/{userId}')
            userRef.update({
                "book" : bookUserWant
            })
            break
        else:
            addNewUser(name,bookUserWant)
            break

#function that handel borrowing book
def borrowBook(name,bookUserWant):
    bookFound = False
    data = ref_available_book.get()
    
    for bookid, bookinfo in data['BookData'].items():
        if bookinfo['Title'] == bookUserWant:
            bookFound = True
            print(f"Thank you {name}! you have to return {bookinfo['Title']} in 30 days")
            
            ref_delet_book = db.reference(f'AvailableBooks/BookData/{bookid}')
            ref_delet_book.delete()
            
            userBorrowBook(name, bookUserWant)
            break
                
    if not bookFound:
        print(f"We do not have {bookUserWant} Sorry!")

#"Updateing user info when user return book"
def userReturnBook(bookUserReturn):  
    usersData = ref_users_data.get()
    for userId, userInfo in usersData.items():
        if userInfo['book'] == bookUserReturn:
            userRef = db.reference(f'Users/UsersData/{userId}')
            userRef.update({
                "book" : "none"
            })
            break
        else:
            break    
 
# "this function is for retruning book"
def returnBook(name,bookUserWant):
    bookUserReturn = input("Which book are you going to return ? : ")
    ref_all_book = db.reference('AllBookData')
    Alldata = ref_all_book.get()
    
    foundBook = False
    
    for bookid, bookinfo in Alldata.items():
        if bookinfo["Title"] == bookUserReturn:
            copiedValue = {bookid : bookinfo}
            ref_available_book.update(copiedValue)
            userReturnBook(bookUserReturn)
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
        ref_available_book.update(newBook)
        print("Thank you visit us again")
        addNewUser(name,bookUserWant)
returnBook("Julia","HT")        
            
# "main functon" 
def main():
    name = str(input("Please eneter your name : "))
    print(f" Hello {name}! How are you! ")
    while True:
        try:
            userChoice = int(input("1.Continue\n2.Quite : "))
            if userChoice == 1:
                print("What would you like to do?")
                try:
                    userInput = int(input("1.Borrow Book\n2.Return Book\n3.User Profile\n4.Quite : "))
                    if userInput == 1:
                        showAvailableBooks()
                        bookUserWant = input("Which book do you want ? : ")
                        borrowBook(name,bookUserWant)
                    elif userInput == 2:
                        bookUserWant = ""
                        returnBook(name,bookUserWant)
                    elif userInput == 3:
                        pass
                    elif userInput == 4:
                        break
                    else:
                        print("Please type number only 1-4")
                except ValueError:
                    print("Please type number only 1,2,3,4")
            elif userChoice == 2:
                print("Thank you visit again!")
                break
            else:
                print("Please type 1,2,3")
        except ValueError:
            print("Please type number only 1,2")

#main()