import json
import random
import string
import firebase_admin
from firebase_admin import credentials, db

# "Firebase Initialization"
cred = credentials.Certificate("D:/Data/Python/New Beginning/cred.json") 
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://onlib-f4bf7-default-rtdb.firebaseio.com/"
})
    
ref_available_books = db.reference('AvailableBooks/BookData')
ref_users_data = db.reference('Users/UsersData')

# "Function to print list of books" 
def show_available_books():
    data = ref_available_books.get()
    for book_id, book_info in data['BookData'].items():
        print(f"{book_info['Title']} by {book_info['Author']}")

# "Add new user"
def add_new_user(name, book_user_wants):
    random_user_id = random.randint(20, 100)
    random_age = random.randint(20, 100)
    new_user = {
        f"user{random_user_id}": {
                "name": name,
                "age": random_age,
                "book": book_user_wants
            }
        }
    ref_users_data.update(new_user)

# "This function will update user data when a user borrows a book"     
def user_borrow_book(name, book_user_wants):
    users_data = ref_users_data.get()
    for user_id, user_info in users_data.items():
        if user_info['name'] == name:
            user_ref = db.reference(f'Users/UsersData/{user_id}')
            user_ref.update({
                "book": book_user_wants
            })
            break
    else:
        add_new_user(name, book_user_wants)

# Function that handles borrowing a book
def borrow_book(name, book_user_wants):
    book_found = False
    data = ref_available_books.get()
    
    for book_id, book_info in data.items():
        if book_info['Title'] == book_user_wants:
            book_found = True
            print(f"Thank you {name}! You have to return {book_info['Title']} in 30 days")
            
            ref_delete_book = db.reference(f'AvailableBooks/BookData/{book_id}')
            ref_delete_book.delete()
            
            user_borrow_book(name, book_user_wants)
            break
                
    if not book_found:
        print(f"We do not have {book_user_wants}. Sorry!")

# "This function is for returning a book"
def return_book(name, book_user_wants):
    book_user_return = input("Which book are you going to return? : ")
    ref_all_books = db.reference('AllBookData')
    all_data = ref_all_books.get()
    found_book = False
    
    for book_id, book_info in all_data['BookData'].items():
        if book_info['Title'] == book_user_return:
            copied_value = {book_id: book_info}
            ref_available_books.update(copied_value)
            
            users_data = ref_users_data.get()
            for user_id, user_info in users_data.items():
                if user_info['name'] == name:
                    user_ref = db.reference(f'Users/UsersData/{user_id}')
                    user_ref.update({
                        "book": "none"
                    })
                else:
                    add_new_user(name, book_user_wants)    
            found_book = True
            print("Thank you! Visit us again.")
            break
            
    if not found_book:
        random_book_id = random.randint(600, 1000)
        random_year = random.randint(1900, 2000)
        random_name = ''.join(random.choices(string.ascii_letters, k=8))
        new_book = {
            f"Book_{random_book_id}": {
                "Title": book_user_return,
                "Author": random_name,
                "Published Year": random_year
                }
            }
        ref_available_books.update(new_book)
        print("Thank you! Visit us again.")
        add_new_user(name, book_user_wants="")

# User profile function to show and add new users
def show_user_profile(name):
    users_data = ref_users_data.get()
    user_found = False
    for user_id, user_info in users_data.items():
        if user_info['name'] == name:
            print(f"Name: {user_info['name']}\nBook: {user_info['book']}")
            user_found = True
            break
            
    if not user_found:
        print(f"User {name} does not have an account")
        add_user = int(input(f"Press 1 to add {name} as a new account? : "))
        if add_user == 1:
            add_new_user(name, book_user_wants="none")
            print(f"New user {name} added.")           
        else:
            print(f"{name} is not in the database.")
                                       
# "Main function" 
def main():
    name = str(input("Please enter your name: "))
    print(f"Hello {name}! How are you?")
    while True:
        try:
            user_choice = int(input("1. Continue\n2. Quit: "))
            if user_choice == 1:
                print("What would you like to do?")
                try:
                    user_input = int(input("1. Borrow Book\n2. Return Book\n3. User Profile\n4. Quit: "))
                    if user_input == 1:
                        user_info_for_book = int(input("1. Show available books\n2. Borrow book by Title? : "))
                        if user_info_for_book == 1:
                            show_available_books()
                        elif user_info_for_book == 2:
                            book_user_wants = input("Enter book name: ")
                            borrow_book(name, book_user_wants)
                        else:
                            print("Please enter a number between 1-2 only.")
                    elif user_input == 2:
                        return_book(name, book_user_wants="")
                    elif user_input == 3:
                        show_user_profile(name)
                    elif user_input == 4:
                        break
                    else:
                        print("Please type a number between 1-4.")
                except ValueError:
                    print("Please type a number between 1, 2, 3, or 4.")
            elif user_choice == 2:
                print("Thank you! Visit again!")
                break
            else:
                print("Please type 1 or 2.")
        except ValueError:
            print("Please type a number between 1 and 2.")

main()
