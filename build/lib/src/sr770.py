import serial

class SR770:
    """
    Class for serial communication with SR770
    """
    port = "/dev/ttyUSB5"
    baud = 9600

    def __init__(self):
        self.serial = serial.Serial(
            SR770.port,
            SR770.baud,
            serial.EIGHTBITS,
            serial.PARITY_NONE,
        )

    def query(self):
        msg_remote = '*IDN?\n'
        #msg_remote = 'CTRF 10E3\n'

        self.serial.write('OUTP 0\n'.encode())
        self.serial.write(msg_remote.encode())
        c = ''
        s = ''
        try:
            while c !=b'\r':
                c = self.serial.read(1)
                s += c.decode()
        except KeyboardInterrupt:
            return float(s)
        else:
            return float(s)


if __name__ == '__main__':
    dev = SR770()
    print(dev.query())
