from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
from cryptography.fernet import Fernet
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
# For testing
ENCRYPTION_KEY = "_miq2TeKiawOU5Hczipg0c4m-V1fx8NQ9KVoWrZ-4yQ="


def generate_key():
    key = Fernet.generate_key()
    key = key.decode()


def encrypt(data):
    message_byte = str.encode(data)
    encrypted = Fernet(ENCRYPTION_KEY).encrypt(message_byte)
    encrypt_string = encrypted.decode("utf-8")
    return encrypt_string


def decrypt(token):
    decrypted = Fernet(ENCRYPTION_KEY).decrypt(token)
    decrypt_string = decrypted.decode("utf-8")
    return decrypt_string


#Password Generator Project
def generate_password():
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
               'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    encrypted_password = encrypt(password)

    #password = password_entry.get()
    new_data = {website: {"email": email, "password": encrypted_password}}

    if website == "" or password == "" or email == "":
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)  # Read existing data

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data) # Add new data to existing data
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ------------------------- Search For Data ---------------------------- #
def find_password(website):
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="error", message="No websites have been saved")
    else:
        if website in data:
            email = data[website]["email"]
            decrypted_password = decrypt(data[website]["password"])
            password = decrypted_password
            messagebox.showinfo(website, f"Email: {email}\n Password: {password}\n Password copied to clipboard")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title=website, message=" not data found")


def delete_password():
    website = website_entry.get()
    email = email_entry.get()

    if website == 0 and email == 0:
        messagebox.showinfo(title=f"Incorrect Data", message="Correct website and email is required")
        print("Error: Website or email were left blank.")
        return

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Password file not found")
    else:
        if website in data:
            data.pop(website)

            with open("data.json", "w") as data_to_save:
                json.dump(data, data_to_save, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)
            messagebox.showinfo(title=f"Success", message="Password deleted!")
        else:
            messagebox.showinfo(title=f"Not found", message="Correct website and email is required")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

#Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1)
email_entry.insert(0, "mail@gmail.com")
password_entry = Entry(width=35)
password_entry.grid(row=3, column=1)

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", width=14, command=lambda: find_password(website_entry.get()))
search_button.grid(column=2, row=1, columnspan=2)
delete_password_button = Button(text="Delete Password", command=delete_password)
delete_password_button.grid(row=2, column=2, columnspan=2)

window.mainloop()