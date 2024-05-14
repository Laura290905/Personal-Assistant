import json
import os
import re
from datetime import datetime, timedelta


class PersonalAssistant:
    def __init__(self, data_dir='data', name='Personal Assistant'):
        self.name = name
        self.data_dir = data_dir
        self.contacts_file = os.path.join(data_dir, 'contacts.json')
        self.notes_file = os.path.join(data_dir, 'notes.json')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.contacts = self.load_data(self.contacts_file)
        self.notes = self.load_data(self.notes_file)

    def load_data(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return []

    def save_data(self, data, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def add_contact(self, name, address, phone, email, birthday):
        if not self.validate_email(email):
            return "Invalid email format."
        if not self.validate_phone_number(phone):
            return "Invalid phone number format."
        contact = {'name': name, 'address': address,
                   'phone': phone, 'email': email, 'birthday': birthday}
        self.contacts.append(contact)
        self.save_data(self.contacts, self.contacts_file)
        return "Contact added successfully."

    def validate_email(self, email):
        pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        return re.match(pattern, email)

    def validate_phone_number(self, phone):
        pattern = r'^\+?[\d\s]+$'
        return re.match(pattern, phone)

    def search_contacts(self, query):
        return [contact for contact in self.contacts if query.lower() in contact['name'].lower()]

    def edit_contact(self, name, new_data):
        for contact in self.contacts:
            if contact['name'].lower() == name.lower():
                contact.update(new_data)
                self.save_data(self.contacts, self.contacts_file)
                return "Contact updated."
        return "Contact not found."

    def delete_contact(self, name):
        original_length = len(self.contacts)
        self.contacts = [
            contact for contact in self.contacts if contact['name'].lower() != name.lower()]
        if len(self.contacts) < original_length:
            self.save_data(self.contacts, self.contacts_file)
            return "Contact deleted."
        return "Contact not found."

    def add_note(self, text, tags=None):
        note = {'text': text, 'tags': tags if tags else []}
        self.notes.append(note)
        self.save_data(self.notes, self.notes_file)
        return "Note added with tags."

    def search_notes_by_text(self, query):
        return [note for note in self.notes if query.lower() in note['text'].lower()]

    def search_notes_by_tags(self, tag_query):
        return [note for note in self.notes if tag_query.lower() in (tag.lower() for tag in note['tags'])]

    def edit_note(self, index, new_text, new_tags=None):
        if 0 <= index < len(self.notes):
            self.notes[index]['text'] = new_text
            if new_tags:
                self.notes[index]['tags'] = new_tags
            self.save_data(self.notes, self.notes_file)
            return "Note updated."
        return "Note index out of range."

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            self.save_data(self.notes, self.notes_file)
            return "Note deleted."
        return "Note index out of range."

    def display_upcoming_birthdays(self, days):
        today = datetime.now()
        upcoming_birthdays = []
        for contact in self.contacts:
            birthday = datetime.strptime(contact['birthday'], "%Y-%m-%d")
            this_year_birthday = birthday.replace(year=today.year)
            if 0 <= (this_year_birthday - today).days < days:
                upcoming_birthdays.append(contact)
        return upcoming_birthdays

    def interact(self):
        print(f"Hello, I am your {
              self.name}. I can help you manage your contacts and notes.")
        print("Options:")
        print("1: Add a contact")
        print("2: Search for a contact")
        print("3: Edit a contact")
        print("4: Delete a contact")
        print("5: Add a note")
        print("6: Search for notes by text")
        print("7: Search for notes by tags")
        print("8: Edit a note")
        print("9: Delete a note")
        print("10: Display upcoming birthdays")
        choice = input(
            "What would you like me to do? (Enter a number or 'exit' to quit): ")
        return choice

    def process_input(self):
        choice = self.interact()
        while choice.lower() != 'exit':
            if choice.isdigit() and 1 <= int(choice) <= 10:
                self.handle_choice(int(choice))
            else:
                print("Invalid choice. Please select a valid option.")
            choice = self.interact()
        print("Goodbye!")

    def handle_choice(self, choice):
        if choice == 1:
            self.add_contact_workflow()
        elif choice == 2:
            self.search_contact_workflow()
        elif choice == 3:
            self.edit_contact_workflow()
        elif choice == 4:
            self.delete_contact_workflow()
        elif choice == 5:
            self.add_note_workflow()
        elif choice == 6:
            self.search_notes_by_text_workflow()
        elif choice == 7:
            self.search_notes_by_tags_workflow()
        elif choice == 8:
            self.edit_note_workflow()
        elif choice == 9:
            self.delete_note_workflow()
        elif choice == 10:
            self.display_upcoming_birthdays_workflow()

    def add_contact_workflow(self):
        name = input("Enter name: ")
        address = input("Enter address: ")
        phone = input("Enter phone number: ")
        email = input("Enter email: ")
        birthday = input("Enter birthday (YYYY-MM-DD): ")
        result = self.add_contact(name, address, phone, email, birthday)
        print(result)

    def search_contact_workflow(self):
        query = input("Enter search query for contacts: ")
        results = self.search_contacts(query)
        for contact in results:
            print(contact)

    def edit_contact_workflow(self):
        name = input("Enter the name of the contact to edit: ")
        existing_contact = next(
            (contact for contact in self.contacts if contact['name'].lower() == name.lower()), None)
        if existing_contact:
            print("Editing contact:", existing_contact)
            new_data = {
                'name': input("Enter new name (or leave blank to keep current): ") or existing_contact['name'],
                'address': input("Enter new address (or leave blank to keep current): ") or existing_contact['address'],
                'phone': input("Enter new phone number (or leave blank to keep current): ") or existing_contact['phone'],
                'email': input("Enter new email (or leave blank to keep current): ") or existing_contact['email'],
                'birthday': input("Enter new birthday (YYYY-MM-DD) (or leave blank to keep current): ") or existing_contact['birthday']
            }
            existing_contact.update(new_data)
            self.save_data(self.contacts, self.contacts_file)
            print("Contact updated successfully.")
        else:
            print("Contact not found.")

    def delete_contact_workflow(self):
        name = input("Enter the name of the contact to delete: ")
        if self.delete_contact(name) == "Contact deleted.":
            print("Contact deleted successfully.")
        else:
            print("Contact not found.")

    def add_note_workflow(self):
        text = input("Enter note text: ")
        tags = input("Enter tags separated by commas (optional): ").split(',')
        print(self.add_note(text, [tag.strip()
              for tag in tags if tag.strip()]))

    def search_notes_by_text_workflow(self):
        query = input("Enter search query for notes by text: ")
        results = self.search_notes_by_text(query)
        for note in results:
            print(note)

    def search_notes_by_tags_workflow(self):
        tag_query = input("Enter tag to search for notes by tags: ")
        results = self.search_notes_by_tags(tag_query)
        for note in results:
            print(note)

    def edit_note_workflow(self):
        text_query = input("Enter the text of the note you want to edit: ")
        matching_notes = [
            note for note in self.notes if text_query.lower() in note['text'].lower()]
        if not matching_notes:
            print("No matching note found.")
        elif len(matching_notes) == 1:
            # Only one matching note found, edit it directly
            note = matching_notes[0]
            new_text = input(
                "Enter new text for the note (leave blank to keep current): ")
            if new_text:
                note['text'] = new_text
            new_tags = input(
                "Enter new tags separated by commas (leave blank to keep current): ").split(',')
            if new_tags[0]:
                note['tags'] = [tag.strip() for tag in new_tags if tag.strip()]
            self.save_data(self.notes, self.notes_file)
            print("Note updated successfully.")
        else:
            # Multiple matching notes found, let the user select one to edit
            print(
                "Multiple notes found. Please select one to edit by entering the corresponding number:")
            for index, note in enumerate(matching_notes):
                print(f"{index + 1}: {note['text']
                                      } - Tags: {', '.join(note['tags'])}")
            try:
                selected_index = int(
                    input("Enter the number of the note to edit: ")) - 1
                if 0 <= selected_index < len(matching_notes):
                    note = matching_notes[selected_index]
                    new_text = input(
                        "Enter new text for the note (leave blank to keep current): ")
                    if new_text:
                        note['text'] = new_text
                    new_tags = input(
                        "Enter new tags separated by commas (leave blank to keep current): ").split(',')
                    if new_tags[0]:
                        note['tags'] = [tag.strip()
                                        for tag in new_tags if tag.strip()]
                    self.save_data(self.notes, self.notes_file)
                    print("Note updated successfully.")
                else:
                    print("Invalid selection. No changes made.")
            except ValueError:
                print("Please enter a valid number.")

    def delete_note_workflow(self):
        index = int(input("Enter the index of the note to delete: "))
        if self.delete_note(index) == "Note deleted.":
            print("Note deleted successfully.")
        else:
            print("Note index out of range or note not found.")

    def display_upcoming_birthdays_workflow(self):
        days = int(
            input("Enter the number of days to check for upcoming birthdays: "))
        results = self.display_upcoming_birthdays(days)
        if results:
            for contact in results:
                print(f"{contact['name']} has a birthday on {
                      contact['birthday']}.")
        else:
            print(f"No birthdays in the next {days} days.")


# To run the interactive personal assistant
if __name__ == '__main__':
    pa = PersonalAssistant()
    pa.process_input()
