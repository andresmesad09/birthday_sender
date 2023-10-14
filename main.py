import smtplib
from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path
import random
import pandas as pd

load_dotenv(override=True)

my_email = os.environ.get("SENDER")
password = os.environ.get("PWD")

# Gather all letters
letter_path = Path().cwd() / "letter_templates"
letters = [letter for letter in letter_path.rglob("*.txt")]

# Read all birthdays
birthdays_file = Path().cwd() / "birthdays.csv"
birthday_df = pd.read_csv(birthdays_file, encoding="utf-8")

today = datetime.today()

# Let's send the letter
for index, person in birthday_df.iterrows():
    person_month = person['month']
    person_day = person['day']
    if person_day == today.day and person_month == today.month:
        # Pick a random letter
        letter_to_open = random.choice(letters)
        with open(letter_to_open, mode="r") as f:
            birthday_msg = f.read().replace('[NAME]', person['name'].title())
        # Send the email
        with smtplib.SMTP("smtp.gmail.com") as connection:
            # to encrypt
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=person['email'],
                msg=f"Subject:Happy Birthday!\n\n{birthday_msg}")
