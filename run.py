import serial
import time
import csv


class Modem:
    def __init__(self, recipients=None, message="Test message", name="COM14", baud="96000"):
        self.recipients = recipients
        self.content = message
        self.name = name
        self.baud = baud
        self.count = 0

    def set_recipients(self, numbers):
        self.recipients = numbers

    def set_content(self, message):
        self.content = message

    def connect(self):
        self.ser = serial.Serial(self.name, self.baud, timeout=5)
        time.sleep(1)

    def send(self, recipient):
        self.ser.write('ATZ\r'.encode())
        # time.sleep(1)
        self.ser.write('AT+CMGF=1\r'.encode())
        # time.sleep(1)
        self.ser.write(('''AT+CMGS="''' + recipient + '''"\r''').encode())
        # time.sleep(1)
        self.ser.write((self.content + "\r").encode())
        # time.sleep(1)
        self.ser.write(chr(26).encode())
        time.sleep(1)
        print(f'Message send successfully to {recipient}')
        self.count += 1

    def send_toall(self):
        for r in self.recipients:
            self.send(r)

    def disconnect(self):
        self.ser.close()

    def count_msg(self):
        print('\n\n')
        print(f'Successfully sent the message to {self.count} recipients!')


contacts = []
with open('contacts.csv', 'r') as f:
    reader = csv.DictReader(f)
    for c in reader:
        p = c['Phone 1 - Value']
        p = p.strip()
        p = p.replace(' ', '')
        p = p[-9:]
        contacts.append(f'+255{p}')
    # print(contacts)

m = Modem(recipients=['+255713123066', '+255719169800', '+255713123066'])
m.connect()
m.send(recipient="+255713123066")
m.send_toall()
m.disconnect()
m.count_msg()
