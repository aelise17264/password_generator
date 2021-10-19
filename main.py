from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    new_password = "".join(password_list)
    password_text.insert(0, new_password)
    pyperclip.copy(new_password)



# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_name.get()
    user = username.get()
    password = password_text.get()
    new_data = {website: {
                    "email": user,
                    "password": password
                    }
                }

    if len(website) ==0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                # read the old data
                data = json.load(data_file)
        except FileNotFoundError:
            # data_file has not been created yet because no users have been created
            with open("data.json", "a") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_name.delete(0, END)
            password_text.delete(0, END)
# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_name.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No info found for {website}")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock = PhotoImage(file="lock.png")
canvas.create_image(100, 100, image=lock)
canvas.grid(column=1, row=0)

website = Label(text="Website")
website.grid(column=0, row=1)

website_name = Entry(width=35)
website_name.grid(column=1, row=1, columnspan=2, sticky=W)
website_name.focus()

user = Label(text="Email/Username", padx=10)
user.grid(column=0, row=2)

username = Entry(width=35)
username.insert(0, "youremail@email.com")
username.grid(column=1, row=2, columnspan=2, sticky=W)

password = Label(text="Password")
password.grid(column=0, row=3)

password_text = Entry(width=21)
password_text.grid(column=1, row=3, sticky=W)

generate = Button(text="Generate Password", command=generate_password)
generate.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()