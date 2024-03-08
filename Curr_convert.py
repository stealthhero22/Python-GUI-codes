import re # For regular expression operations
import datetime # For handling dates and times
import requests # For making HTTP requests to web services
from tkinter import * # For creating GUI components
import tkinter as tk # For accessing tkinter's functions and variables with tk prefix
from tkinter import ttk # For accessing tkinter's themed widgets
from PIL import Image, ImageTk # For image processing and displaying in tkinter


class RealTimeCurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json() # Fetching currency data from the API
        self.currencies = self.data['rates'] # Storing currency rates fromm the API response

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != 'USD': # Convert to USD if from_currency is not USD
            amount = amount / self.currencies[from_currency]

        # limiting the precision to 4 decimal places
        amount = round(amount * self.currencies[to_currency], 4) # Convert to target currency and round off
        return amount


class App(tk.Tk):
    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title('Currency Converter by Rohan') # Window title
        self.configure(bg='#000000') # Background color
        self.currency_converter = converter # Instance of a currency converter class
        self.geometry("500x250") # Window size

        # Navbar frame
        self.navbar_frame = tk.Frame(self, height=50, bg="blue")
        self.navbar_frame.pack(fill=tk.X)

        # Loading the image
        self.logo_image = Image.open("logo.jpg")
        self.logo_image = self.logo_image.resize((50, 50))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Placing the image in the navbar
        self.logo_label = tk.Label(self.navbar_frame, image=self.logo_photo, bg="blue")
        self.logo_label.pack(side=tk.LEFT, padx=10)

        # Label
        self.intro_label = Label(self, text='Convert Currency', fg='blue', relief=tk.RAISED, borderwidth=3)
        self.intro_label.config(font=('Verdana', 15, 'bold'))
        api_date = self.currency_converter.data['date']
        datetime.datetime.strptime(api_date, '%Y-%m-%d').strftime('%m/%d/%Y')

        self.date_label = Label(self,
                                text="Enter Currency type and amount",
                                relief=tk.GROOVE, borderwidth=5)

        self.intro_label.place(x=200, y=10)
        self.date_label.place(x=160, y=60)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self, bd=3, relief=tk.RIDGE, justify=tk.CENTER, validate='key', validatecommand=valid)
        self.converted_amount_field_label = Label(self, text='', fg='black', bg='white', relief=tk.RIDGE,
                                                  justify=tk.CENTER, width=17, borderwidth=3)

        # dropdown
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("USD")
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("EUR")

        font = ("Courier", 12, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,
                                                   values=list(self.currency_converter.currencies.keys()), font=font,
                                                   state='readonly', width=12, justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,
                                                 values=list(self.currency_converter.currencies.keys()), font=font,
                                                 state='readonly', width=12, justify=tk.CENTER)

        # placing
        self.from_currency_dropdown.place(x=30, y=120)
        self.amount_field.place(x=36, y=150)
        self.to_currency_dropdown.place(x=340, y=120)
        self.converted_amount_field_label.place(x=346, y=150)

        # Convert button with Unicode character
        self.convert_button = Button(self, text=u"\u27A1", fg="black", bg='yellow', command=self.perform)
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x=225, y=135)

    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_field_label.config(text=str(converted_amount))

    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))


if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url) # Creating an instance of the converter
    App(converter) # Creating an instance of the App class
    mainloop() # Starts the tkinter event loop
