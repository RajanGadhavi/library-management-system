import json
import json5

users1 = {
    "users1": {
        "user1": {
            "name": "Alice",
            "age": 25
        },
        "user2": {
            "name": "Bob",
            "age": 30
        },
        "user3": {
            "name": "Charlie",
            "age": 22
        }
    }
}

users2 = {
    "users20":{
        "user4": {
            "name": "Diana",
            "age": 28
        },
        "user5": {
            "name": "Ethan",
            "age": 24
        }
    }
}

names = "Charlie"

for users, name in users1["users1"].items():
    if name["name"] == names:
        print(users)
        value = users
        users2["users20"][users] = name

print(users2)
print(json.dumps(users2, indent=4))
