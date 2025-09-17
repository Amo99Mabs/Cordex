import json
import re
from typing import Dict, Optional

DATA_FILE = "contacts.json"

def load_contacts() -> Dict[str, str]:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
    except FileNotFoundError:
         pass
    except (json.JSONDecodeError, OSError):
         print("Warning: could not read contacts file - starting with an empty contact book.")
         return  {}



def save_contacts(contacts: Dict[str : str]) -> None:
    try:
         with open (DATA_FILE, "w", encoding="utf-8") as fh:
              json.dump(contacts, fh, ensure_ascii=False, indent=2)
    except OSError:
         print("Error: failed to save contacts.")



def normalize_for_lookup(name: str) -> str:
     return name.strip().casefold()


def find_contact_key(contacts: Dict[str: str],query_name: str) -> Optional[str]:
     lookup = normalize_for_lookup(query_name)
     for stored_name in contacts:
          if normalize_for_lookup(stored_name) == lookup:
               return stored_name
     return None


def valid_phone_number(phone: str) -> bool:
     phone_s = phone = phone.strip()
     pattern = re.compile(r"^\+?[\d\s\-]{7,20}$")
     return bool(pattern.fullmatch(phone_s))


def display_contacts(contacts: Dict[str : str]) -> None: 
    if not contacts:
         print("\nContact book is empty.\n")
         return
    print("\nName\t\tContact Number")
    print("-" * 40)
    for name in sorted(contacts):
        print(f"{name}\t\t{contacts[name]}")
        print()


while True:
    choice = int(input("1.Add new contact➕  \n 2. Search contact🔍 \n 3. Display contact📃\n 4. Edit contact✍️\n 5. Delete contact🚮 \n 6. Exit🚶‍♂️\n Enter your choice "))
    if choice == 1:
        name = input("Enter the contact name 🔤 ")
        phone = input("Enter the mobile number 📱 ")
        contact[name] = phone
    elif choice == 2:
        search_name = input("Enter the contact name ")
        if search_name in contact:
            print(search_name,"'s contact number is",contact[search_name])
        else:
            print("Name is not found in contact book")
    elif choice == 3:
            if not contact:
                print("empty contact book ")
            else:
                display_contact()
    elif choice == 4:
            edit_contact = input("Enter the contact to be edited")
            if edit_contact in contact:
                 phone = input("enter mobile number ")
                 contact[edit_contact]=phone
                 print("contact updated!")
                 display_contact()
            else:
                 print("Name is not found in contact book!")
    elif choice == 5:
            del_contact = input("Enter the contact to be deleted ")
            if del_contact in contact:
                confirm = input("Do you want to delete this contact y/n? ")
                if confirm == 'y' or confirm == 'Y':
                    contact.pop(del_contact)
                display_contact()
            else:
                print("Name is not found in contact book 🥲")
    else:
        break


