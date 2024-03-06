from collections import UserDict

# Decorator for error handling


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except KeyError:
            return "Contact not found."
        except IndexError:
            # Check which function raised the exception to provide a context-specific message
            if func.__name__ == 'add_contact':
                return "Please provide a name and phone number."
            elif func.__name__ == 'change_contact':
                return "Please provide a name, old phone number, and new phone number."
            elif func.__name__ == 'show_phone':
                return "Please provide a name to search."
            else:
                return "Missing arguments."
    return inner

# Classes for managing the address book


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format. Must be 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Phone number not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def change_phone(self, new_phone):
        if self.phones:
            self.phones[0] = Phone(new_phone)
        else:
            raise ValueError("No phone number to change.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Record not found.")

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

# Functions for the virtual assistant


@input_error
def add_contact(book):
    user_input = input(
        "Enter username and phone number separated by a space: ")
    name, phone = user_input.split()
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."


@input_error
def change_contact(book):
    user_input = input(
        "Enter username and new phone number separated by a space: ")
    name, new_phone = user_input.split()
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.change_phone(new_phone)
    return "Contact updated."


@input_error
def show_phone(book, username):
    record = book.find(username)
    if record is None:
        return "Contact not found."
    return str(record)


def show_all_contacts(book):
    return str(book)


def parse_input(user_input):
    parts = user_input.split(maxsplit=1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    return cmd, args


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(book))
        elif command == "change":
            print(change_contact(book))
        elif command == "phone":
            if args:
                print(show_phone(book, args.strip()))
            else:
                print("Please provide a username.")
        elif command == "all":
            print(show_all_contacts(book))
        else:
            print("Invalid command.")


# if __name__ == "__main__":
    main()


# Creation of a new address book
book = AddressBook()

# Creation of a entry for John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Add a John entry to the address book
book.add_record(john_record)

# Creating and adding a new entry for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Displaying all entries in the contact list
for name, record in book.data.items():
    print(record)

# Find and edit a phone number for John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Displaying: Contact name: John, phones: 1112223333; 5555555555

# Searching for a specific phone number in John's entry
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")
# Deletion: 5555555555

# Deletion Jane's entry
book.delete("Jane")
