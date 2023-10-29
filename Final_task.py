import re
from Address_book import AddressBook, Record


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me the correct data"
    return wrapper

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone = args
    if name.lower() in book.data:
        return ("Contact already exists")
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

@input_error
def change_username_phone(args, book):
    name, new_phone = args
    pattern = re.compile(r'\d{10}$')
    if not re.match(pattern, new_phone):
        raise ValueError (print("Phone number must have 10 digits in format 0501111111"))
    if name.lower() in book.data:
        record = book.data[name.lower()]
        record.edit_phone(record.phones[0].value, new_phone)
        return "Contact updated."
    else:
        return "No such username"
        
@input_error
def phone_username(args, book):
    if args:
        name = args[0]
        if name.lower() in book.data:
            record = book.data[name.lower()]
            return record.phones[0]
        else:
            return "No such username"
    else:
        raise ValueError (print("Wrong format, please enter the data in format: phone <name>"))

@input_error    
def all(book):
    if book.data:
        result = ''
        for _, value in book.data.items():
            result += str(value) + "\n"
        return result
    else:
        raise ValueError (print("The list of contacts is empty, please enter add <name> <phone>"))
      
@input_error
def add_birthday(args, book):
    name, birthday = args
    if name.lower() in book.data:
        record = book.data[name.lower()]
        record.add_birthday(birthday)
        return "Birthday added"
    else:
        return "No such username"

@input_error
def show_birthday(args, book):
    if args:
        name = args[0]
        if name.lower() in book.data:
            record = book.data[name.lower()]
            return record.birthday
        else:
            return "No such username"
    else:
        raise ValueError (print("Wrong format, please enter the data in format: show-birthday <name>"))
   
@input_error
def birthdays(book):
    birthdays = book.get_birthdays_per_week()
    if birthdays:
        return birthdays
    else:
        return "No birthdays next week"

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input) 
        
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command in ["hello", "hi"]:
            print("""How can I help you?
                For adding the contact please enter the data in format: add <name> <phone> (10 digits in format 0501111111)
                For changing the contact please enter the data in format: change <name> <new phone> (10 digits in format 0501111111)
                For getting a phone number please enter the data in format: phone <name>
                For adding a birthday please enter the data in format: add-birthday <name> birthday (in format DD.MM.YYYY)
                For getting user's birthday please enter the data in format: show-birthday <name>
                For getting a list of next week's birthdays enter <birthdays>
                For getting the list of all contacts enter: <all>
                For exit please enter: <close> or <exit> """)
        elif command in ["add"]:
            print(add_contact(args, book))
        elif command in ["change"]:
            print(change_username_phone(args, book))
        elif command in ["phone"]:
            print(phone_username(args, book))
        elif command in ["all"]:
            print(all(book))
        elif command in ["add-birthday"]:
            print(add_birthday(args, book))
        elif command in ["show-birthday"]:
            print(show_birthday(args, book))
        elif command in ["birthdays"]:
            print(birthdays(book))
        else:
            print("Invalid command. Please verify the command and try again")
    

if __name__ == "__main__":
    main()  
