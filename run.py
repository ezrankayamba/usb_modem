import serial
import time
import csv


class Modem:
    def __init__(self, recipients=None, message_parts=None, name="COM14", baud="115200"):
        self.recipients = recipients
        self.message_parts = message_parts
        self.name = name
        self.baud = baud
        self.count = 0

    def set_recipients(self, numbers):
        self.recipients = numbers

    def set_content(self, message_parts):
        self.message_parts = message_parts

    def read_res(self):
        res = []
        print('Reading response...')
        while True:
            line = self.ser.readline()
            # print(line)
            res.append(line)
            if line.startswith(b'OK'):
                break
        print(res)
        return res

    def connect(self):
        self.ser = serial.Serial(self.name, self.baud, timeout=1)
        if self.ser:
            self.ser.write('ATZ\r'.encode())
            self.read_res()
            self.ser.write('AT+CSCA?\r'.encode())
            for line in self.read_res():
                if line.startswith(b'+CSCA:'):
                    parts = str(line).split(" ")[1][:-5]
                    self.smsc = parts
                    break

        time.sleep(1)

    def send_pdu(self, res):
        pdu_len, smsc, tpdu = res
        # print(pdu_len, smsc, tpdu)
        # print(f'{pdu_len}{smsc}{tpdu}')
        self.ser.write('ATZ\r'.encode())
        self.ser.write('AT+CMGF=0\r'.encode())
        self.read_res()
        self.ser.write('AT+CSCS="GSM"\r'.encode())
        self.read_res()
        self.ser.write((f'AT+CMGS={pdu_len}\r{smsc}{tpdu}{chr(26)}').encode())
        self.read_res()
        print(f'Message sent successfully as {res}')
        self.count += 1

    def send(self, recipient):
        self.ser.write('ATZ\r'.encode())
        # time.sleep(1)
        self.ser.write('AT+CMGF=1\r'.encode())
        # time.sleep(1)
        for content in self.message_parts:
            self.ser.write(('''AT+CMGS="''' + recipient + '''"\r''').encode())
            # time.sleep(1)
            self.ser.write((content + "\r").encode())
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
with open('../contacts.csv', 'r') as f:
    reader = csv.DictReader(f)
    for c in reader:
        p = c['Phone 1 - Value']
        p = p.strip()
        p = p.replace(' ', '')
        p = p[-9:]
        contacts.append(f'+255{p}')
    contacts.append('+255713123066')
    # print(contacts)
msg_parts = []
# print("How many parts?")
# n = int(input())
# for i in range(n):
#     print(f'\nEnter part {i+1}')
#     msg_parts.append(input())
# if len(msg_parts):
#     m = Modem(recipients=contacts, message_parts=msg_parts)
#     m.connect()
#     # m.send(recipient="+255713123066")
#     m.send_toall()
#     m.disconnect()
#     m.count_msg()

# Test PDU
import util
m = Modem(recipients=contacts, message_parts=msg_parts)
m.connect()
# m.send(recipient="+255713123066")
res = util.at_cmgs(m.smsc, '+255658402406', '+255713123066', 'It is easy to send text messages.')
print(res)
m.send_pdu(res)
m.disconnect()
# m.count_msg()
