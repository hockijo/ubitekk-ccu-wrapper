import serial
import numpy
import time

class CCU():
    def __init__(self):
        pass

    def connect(self, address: str):
        self.device = serial.Serial(address, 
                                    baudrate=19200, 
                                    bytesize=8, 
                                    parity="N",
                                    stopbits=1,
                                )
        
    def close(self):
        self.device.close()

    def send_command(self, command:str):
        self.device.write(bytes(command+'\r', 'utf-8'))

    def read_response(self):
        response = self.device.readline().decode('utf-8').strip('\n')
        if response == "Unknown Command":
            raise RuntimeError(response)
        else:
            return response

    def read_count(self, channel: str):
        if channel.upper()=="CH1":
            self.send_command("COUN:C1?")
        elif channel.upper()=="CH2":
            self.send_command("COUN:C2?")
        elif channel.upper()=="COINCIDENCE":
            self.send_command("COUN:CO?")
        else:
            raise ValueError(channel + "is an invalid channel")

        time.sleep(0.3)
        return int(self.read_response())

    def append_counts_to_csv(self, filename, channels:str='all'):
        ch1 = self.read_count("CH1")
        ch2 = self.read_count("CH2")
        coincidence = self.read_count("COINCIDENCE")

        with open(filename, '+a') as f:
            f.write("{},{},{}\n".format(ch1, ch2, coincidence))


if __name__=="__main__":
    ccu = CCU()
    ccu.connect("/dev/ttyUSB0")
    ccu.append_counts_to_csv("counts.csv")
    ccu.close()