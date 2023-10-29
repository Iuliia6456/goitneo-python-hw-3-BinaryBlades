from collections import UserDict, defaultdict
import re
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validated_phone()

    def validated_phone(self):
        pattern = re.compile(r'\d{10}$')
        if not re.match(pattern, self.value):
            raise ValueError(print("Phone number must have 10 digits in format 0501111111"))


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validated_birthday()

    def validated_birthday(self):
        try:
            datetime.strptime(self.value, "%d.%m.%Y")
        except ValueError:
            raise ValueError(print("Wrong format, must be DD.MM.YYYY"))


class Record:
    def __init__(self, name):
        self.name = Name(name.lower())
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def edit_phone(self, old, new):
        self.phones = [new if str(i) == old else i for i in self.phones]

    def remove_phone(self, phone):
        for i in self.phones:
            if str(i) == phone:
                return self.phones.remove(i)

    def find_phone(self, phone):
        for i in self.phones:
            if str(i) == phone:
                return i
        return "The phone is not found"

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        lower_name = name.lower()
        if lower_name in self.data:
            return self.data[lower_name]
        return "The user is not found"

    def delete(self, name):
        lower_name = name.lower()
        if lower_name in self.data:
            return self.data.pop(lower_name)

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        next_week_birthdays = defaultdict(list)

        for name, record in self.data.items():
            if record.birthday is not None:
                birthday = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                this_year_birthdays = birthday.replace(year=today.year)
                if this_year_birthdays < today:
                    this_year_birthdays = this_year_birthdays.replace(year=today.year + 1)

                delta_days = (this_year_birthdays - today).days
                weekdays = this_year_birthdays.strftime("%A")

                if delta_days < 7 and (weekdays == "Saturday" or weekdays == "Sunday"):
                    weekdays = "Monday"
                    next_week_birthdays[weekdays].append(name)
                elif delta_days < 7 and weekdays in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                    next_week_birthdays[weekdays].append(name)
                else:
                    return "No birthdays next week"
            else:
                return "No birthdays next week"

        result = ''
        for weekdays, names in next_week_birthdays.items():
            result += f"{weekdays}: {', '.join(names)}\n"

        return result
