
from tkinter import *
from tkinter import messagebox
import pyperclip
import random
import json

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = random.randint(8, 10) #password can have 8-10 letters
nr_symbols = random.randint(2, 4) #pass can have 2-4 symbols
nr_numbers = random.randint(2, 4) #pass can have 2-4 numbers


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_letters = [random.choice(letters) for _ in range(nr_letters)] #using list comprehension
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers #adding all three fields to password list
    random.shuffle(password_list)

    password = "".join(password_list)#converting list to a string 
    # for char in password_list:
    #     password += char
    password_entry.insert(0,password)
    pyperclip.copy(password)
    # print(f"Your password is: {password}") just to cross check


def search_password():
    website = website_entry.get() #getting entries data
    if len(website) == 0:
        messagebox.showinfo(title="Oops",message="Don't Leave any of the Field Empty!.")
        return

    try:
        with open("data.json","r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"] 
            password = data[website]["password"]   
            messagebox.showinfo(title=f"{website}", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error",message=f"Details for {website} does not exists.")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get() #getting entries data
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
         website: {
            "email":email,
            "password":password,
        }
    }

    if len(website)==0 or len(password)==0 or len(email) == 0:
        messagebox.showinfo(title="Oops",message="Don't Leave any of the Field Empty!.")
        
    else:
        # is_ok = messagebox.askokcancel(title=website,message=f" Website: {website}\n Email: {email}\n Password: {password}\n Want to save?")

        # if is_ok:
        try:
            with open("data.json" ,"r") as data_file: # working with "with" keyword automatically closes file after use
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json" ,"w") as data_file:   
                json.dump(new_data,data_file,indent=4)                     
        else:
            data.update(new_data)
            with open("data.json" ,"w") as data_file:   
                json.dump(data,data_file,indent=4) 
                # data_file.write(f"{website} | {password} | {email}\n" )
        finally:
                website_entry.delete(0,END)
                password_entry.delete(0,END)
                messagebox.showinfo(title="Success",message="Details Added Successfully.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", height=2,font=("courier",12,"bold"))
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", height=2,font=("courier",12,"bold"))
email_label.grid(row=2, column=0)
password_label = Label(text="Password:", height=2,font=("courier",12,"bold"))
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=54)
email_entry.grid(row=2, column=1, columnspan=3)
email_entry.insert(0,"adnan@gmail.com")
password_entry = Entry(width=35)
password_entry.grid(row=3, column=1,columnspan=2)

# Buttons
generate_password_button = Button(text="Generate",width=14,command=generate_password,bg="lightblue",font=("courier",9))
generate_password_button.grid(row=3, column=3)  # Added padx and pady for spacing
add_button = Button(text="Add", width=45,command=save,padx=2,pady=2,bg="lightblue",font=("courier",9))
add_button.grid(row=4, column=1, columnspan=3)
search_button = Button(text="Search",width=14,command=search_password,bg="lightblue",font=("courier",9))
search_button.grid(row=1, column=3, columnspan=1)


window.mainloop()


