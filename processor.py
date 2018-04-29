import serial
import time
import thingspeak

serial_port = "COM13"
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)
print("Serial port " + serial_port + " opened Baudrate " + str(baud_rate))

start_marker = 60
end_marker = 62

print(ord(b'<'))

def recieve_from_arduino():
    global start_marker, end_marker

    msg = ""
    c = "-"
    byte_count = -1

    while ord(c) != start_marker:
        c = ser.read().decode('utf-8')

    while ord(c) != end_marker:
        if ord(c) != start_marker:
            msg = msg + str(c)
            byte_count += 1
        c = ser.read().decode('utf-8')

    return msg

def wait_for_arduino():
    global start_marker, end_marker
    
    msg = ""
    while msg.find("Arduino is ready") == -1:
      #while ser.inWaiting() == 0:
      #  pass
        
      msg = recieve_from_arduino()

      print(msg)

print("wait..")
wait_for_arduino()
print("done waiting..")

ch = thingspeak.Channel(474625, "A0SH7A9FQQI7JN30", "GDBCRJPIKTEFXRJ3")

while True:
    msg = recieve_from_arduino()
    msg = list(map(int, msg.split(',')))
    ch.update({'field1':msg[0], 'field2':msg[1], 'field3':msg[2]})
    print(msg)
