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



def save_contacts(contacts: Dict[str, str]) -> None:
    try:
         with open (DATA_FILE, "w", encoding="utf-8") as fh:
              json.dump(contacts, fh, ensure_ascii=False, indent=2)
    except OSError:
         print("Error: failed to save contacts.")



def normalize_for_lookup(name: str) -> str:
     return name.strip().casefold()


def find_contact_key(contacts: Dict[str, str],query_name: str) -> Optional[str]:
     lookup = normalize_for_lookup(query_name)
     for stored_name in contacts:
          if normalize_for_lookup(stored_name) == lookup:
               return stored_name
     return None


def valid_phone_number(phone: str) -> bool:
     phone_s = phone = phone.strip()
     pattern = re.compile(r"^\+?[\d\s\-]{7,20}$")
     return bool(pattern.fullmatch(phone_s))


def display_contacts(contacts: Dict[str,  str]) -> None:
    if not contacts:
         print("\nContact book is empty.\n")
         return
    print("\nName\t\tContact Number")
    print("-" * 40)
    for name in sorted(contacts):
        print(f"{name}\t\t{contacts[name]}")
        print()

def add_contact(contact: Dict[str, str]) -> None:
    name = input("Enter the contact name 🔤: ").strip()
    if not name:
        print("Name cannot be empty.\n")
        return
    existing_key = find_contact_key(contacts, name)
    if existing_key:
         print(f"'{existing_key}' already exists. Use edit to change the number or choose another name.\n")
         return
    phone = input("Enter the mobile number 📱: ").strip()
    if not valid_phone_number(phone):
         print("Invalid phone number format. Use didits, optional leading '+', spaces or dashes (7-20 chars).\n")
         return

    contacts[name] = phone
    save_contacts(contacts)
    print(f"Contact '{name}' added.\n")

def search_contact(contacts: Dict[str, str]) -> None:
    name = input("Enter the contact name to search 🔎: ")
    if not name:
         print("Search name cannot be empty.\n")
    else:
         print("Nmae is not found in contact book.\n")


def edit_contact(contacts: Dict[str, str]) -> None:
    name = input("Enter the contact name to edit ✍️: ").strip()
    if not name:
         print("Name cannot be empty.\n")
         return
    key = find_contact_key(contacts, name)
    if not key:
         print("Name is not found in contact book!\n")
         return
    new_phone = input(f"Enter new mobile number for '{key}': ").strip()
    if not valid_phone_number(new_phone):
         print("Invalid phone number. Edit cancelled.\n")
         return
    contacts[key] = new_phone
    save_contacts(contacts)
    print("Contact updated!\n")
    display_contacts(contacts)

def delete_contact(contacts: Dict[str, str]) -> None:
    name = input("Enter the contact to be deleted 🚮: ").strip()
    if not name:
         print("Name is not found in contact book 🥲\n")
         return
    confirm  = input(f"Do you want to delete '{key}'? (y/n): ").strip().lower()
    if confirm  == "y":
         contacts.pop(key)
         save_contacts(contacts)
         print("f'{key}' deleted.\n")
         display_contacts(contacts)
    else:
         print("Deletion cancelled.\n")

def get_choice() -> int:
    menu = (
          "1.Add new contact➕ \n"
          "2. Search contact🔍 \n "
          "3. Display contact📃\n "
          "4. Edit contact✍️\n "
          "5. Delete contact🚮\n"
          "6. Exit🚶‍♂️\n"
          "Enter your choice: "
    )
    while True:
        raw = input(menu).strip()
        if not raw:
             print("Please enter a choice (1-6).\n")
             continue
        if raw.isdigit():
             choice = int(raw)
             if 1 <= choice <= 6:
                  return choice
        print("Invalid input. Enter a number between 1 and 6.\n")

def main() -> None:
    print("Welcome to Cordex!\n")
    contacts = load_contacts()
    while True:
         choice = get_choice()
         if choice == 1:
              add_contact(contacts)
         elif choice == 2:
              search_contact(contacts)
         elif choice == 3:
              display_contacts(contacts)
         elif choice == 4:
              edit_contacts(contacts)
         elif choice == 5:
              delete_contact(contacts)
         elif choice == 6:
             print("Goodbye 👋")
             break


if __name__ == "__main__":
    main()