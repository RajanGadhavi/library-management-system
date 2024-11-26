import json
import firebase_admin
from firebase_admin import credentials, db, firestore 

#Firebase here
cred = credentials.Certificate(r"D:\Data\Python\New Begging\cred.json")  # Replace with the path to your JSON key
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://onlib-f4bf7-default-rtdb.firebaseio.com/"
})

#Books data stored on local storge to firebase 
#filePath = r"D:\Data\Python\New Begging\booksData.json"
#with open(filePath, "r") as file:
    #books_dict = json.load(file)
    
ref = db.reference('/')
#ref.set(books_dict)
data = ref.get()

# "this function is to print list of books" 
def showAvailableBooks():
    for bookid, bookinfo in data["BookData"].items():
        print(f"{bookinfo['Title']} by {bookinfo['Author']} and id is {bookid}")
        
# "this function greet user"
def greetigs(name):
     print(f"Hello!{name} how are you?")
     showAvailableBooks()

def borrowBook():
    bookUserWant = input("Which book do you want ? : ")
    for bookid, bookinfo in data["BookData"].items():
        if bookinfo['Title'] == bookUserWant:
            print(f"Thank you! you have to return {bookinfo['Title']} in 30 days")
            refForBorrow = db.reference(f'BookData/{bookid}')
            refForBorrow.delete()
        elif bookinfo['Title'] != bookUserWant:
            print(f"We do not have {bookUserWant}")

borrowBook()
    

# "main functon" 
def main():
    name = input(str("Your name is : "))
    greetigs(name)
    while True:
        try:
            userChoice = int(input("Which opreation will you perform ?\n1.Borrow books\n2.Return books\n3.Quit : "))
            if userChoice == 1:
                pass
            elif userChoice == 2:
                pass
            elif userChoice == 3:
                print("Thank you visit again!")
                break
            else:
                print("Please type 1,2,3")
        except ValueError:
            print("Please type number only 1,2,3")


