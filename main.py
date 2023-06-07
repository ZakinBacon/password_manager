from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)  # uses Join to add the list to a string

    password_entry.insert(0, password)  # replaces the entry with the password generated
    pyperclip.copy(password)  # saves the password to your clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # Checks if any of the boxes are empty and returns an error
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please dont leave any fields empty")
        return

    # Pop up box to confirm the info before saving it
    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:"
                                                          f" \nEmail: {email} \nPassword {password} \nIs it ok to save?")

    if is_ok:
        try:
            # saves info to txt file
            with open("password_manager.json", "r") as data_file:
                # How to read a json file
                data = json.load(data_file)
        except FileNotFoundError:
            with open("password_manager.json", "w") as data_file:
                # How to write to a file using json
                json.dump(new_data, data_file, indent=4)
        else:
            # updating the old data with new data
            data.update(new_data)
            with open("password_manager.json", "w") as data_file:
                # How to write to a file using json
                json.dump(data, data_file, indent=4)
        finally:
            # data_file.write(f"{website} | {email} | {password} \n")
            # Puts the Entries back to empty
            website_entry.delete(0, END)
            password_entry.delete(0, END)

def find_password():
    website = website_entry.get()
    try:
        with open("password_manager.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
# Creates window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Creates the canvas for the image
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# ----------Titles---------------#

website_name = Label(text="Website:")
website_name.grid(column=0, row=1, padx=20, pady=20, sticky='E')

email_title = Label(text="Email/Username:")
email_title.grid(column=0, row=2, padx=20, pady=20, sticky='E')

password_title = Label(text="Password:")
password_title.grid(column=0, row=3, padx=20, pady=20, sticky='E')

# -------------Entries for info-----------------#

website_entry = Entry(width=70)
website_entry.grid(column=1, row=1, columnspan=2, padx=20, pady=20, sticky='NW')
website_entry.focus() # Auto selects this entry when the program is run

email_entry = Entry(width=70)
email_entry.grid(column=1, row=2, columnspan=2, padx=20, pady=20, sticky='NW')
email_entry.insert(END, "Zach@gmail.com") # Sets the default to be this email

password_entry = Entry(width=50)
password_entry.grid(column=1, row=3, padx=20, pady=20, sticky='NW')

# --------------Buttons-----------------#
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=60, command=save_info)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=20, command=find_password)
search_button.grid(column=2, row=1, columnspan=2)

window.mainloop()
