from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_code():
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [choice(letters) for char in range(randint(8, 10))]
    password_symbols = [choice(symbols) for char in range(randint(2, 4))]
    password_num = [choice(numbers) for char in range(randint(2, 4))]
    password_list = password_letter + password_symbols + password_num

    shuffle(password_list)

    password = "".join(password_list)
    pass_inbox.insert(0, f"{password}")
    pyperclip.copy(f"{password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = web_inbox.get()
    email = email_inbox.get()
    password = pass_inbox.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }}

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="error", message="please do not leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"is this ok? \n email : {email} \n password: {password}"
                                                              f"\n press ok to save data?")
        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            except json.decoder.JSONDecodeError:
                print("all data in json file is deleted please delete previous json file")
            else:
                data.update(new_data)
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                web_inbox.delete(0, END)
                pass_inbox.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
def search():
    website = web_inbox.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="error", message="file not found")
        web_inbox.delete(0, END)
    else:
        if website in data:
            data_dic = data[website]
            email = data_dic["email"]
            password = data_dic["password"]
            messagebox.showinfo(title=website, message=f"email: {email} \npassword: {password}")
        else:
            messagebox.showerror(title="ERROR", message=f"no details for this {website}")


# ---------------------------- search SETUP ------------------------------- #

window = Tk()
window.title("password manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

web_text = Label(text="website:")
web_text.grid(column=0, row=1)

email_txt = Label(text="Email/username:")
email_txt.grid(column=0, row=2)

pass_txt = Label(text="password:")
pass_txt.grid(column=0, row=3)

web_inbox = Entry()
web_inbox.grid(column=1, row=1)
web_inbox.focus()

email_inbox = Entry(width=39)
email_inbox.grid(column=1, row=2, columnspan=2)
email_inbox.insert(0, "xyz@gmail.com")

pass_inbox = Entry(width=21)
pass_inbox.grid(column=1, row=3)

generate_button = Button(text="Generate Password", command=generate_code)
generate_button.grid(column=2, row=3)

add = Button(text="add", width=34, command=save)
add.grid(column=1, row=4, columnspan=2)

search_button = Button(text="search", width=15, command=search)
search_button.grid(column=2, row=1)

window.mainloop()
