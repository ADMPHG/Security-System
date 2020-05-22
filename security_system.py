import smtplib, ssl
import pyfirmata
import time

#defining mail variables
port = 465  #for ssl
smtp_server = 'smtp.gmail.com'
sender_email = 'email@gmail.com' #enter your email address to send alert from
password = 'password' #enter password of sender email account
receiver_email = 'email@gmail.com' #enter email address to receive alert
alert_message = '''\
Subject: Alert!

Motion sensor tripped!'''

#defining pyfirmata variables
board = pyfirmata.ArduinoMega('COM4')
pir_output = board.get_pin('d:7:i')
it = pyfirmata.util.Iterator(board)

#user-defined functions
def send_email():
    print ('Motion Detected! Sending Email')
    context = ssl.create_default_context() #create secure ssl connection
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server: #using 'with smtplib.SMTP_SSL() as server: makes sure that the connection is automatically colsed at the end of the indented code block.
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, alert_message)
        
def buzzLED_pulse():
    board.digital[13].write(1)
    board.digital[12].write(1)
    time.sleep(0.2) #change to increase/decrease on state
    board.digital[13].write(0)
    board.digital[12].write(0)
    time.sleep(0.1) #change to increase/decrease off state

#start of program
it.start()

print ('Initialising...')
time.sleep(60) #PIR sensor needs 60 seconds to warm up.
print ('Armed')
    
while True:
    message = pir_output.read()
    if message == True:
        send_email()
        for x in range (20): #LED blinks and buzzer buzzes x times
            buzzLED_pulse()
        
        time.sleep(60) #Limit no. of emails sent to 1 per minute
    
    time.sleep(0.5) #prevent cpu overload
