import serial
import numpy
import time

class CCU():
    """
    Class for interacting with the CCU.

    Args:
        query_delay (float): The delay in seconds before reading queries.

    """
    def __init__(self, query_delay:float=0.3):
        """
        Initialize the object with a query delay.

        Args:
            query_delay (float): The delay in seconds before reading queries.

        Returns:
            None
        """
        self.query_delay = query_delay
        pass

    def connect(self, address: str):
        """
        Connect to a device using the given address.

        Parameters:
            address (str): The address of the device to connect to.

        Returns:
            None
        """
        self.device = serial.Serial(address, 
                                    baudrate=19200, 
                                    bytesize=8, 
                                    parity="N",
                                    stopbits=1,
                                )
        
    def close(self):
        """
        Closes the device.
        """
        self.device.close()

    def send_command(self, command:str):
        """
        Send a command to the device.

        Args:
            command (str): The command to be sent.

        Returns:
            None
        """
        self.device.write(bytes(command+'\r', 'utf-8'))

    def read_response(self):
        """
        Reads the response from the device and returns it. 

        Returns:
            str: The response from the device.
        
        Raises:
            RuntimeError: If the response is "Unknown Command".
        """
        time.sleep(self.query_delay)
        response = self.device.readline().decode('utf-8').strip('\n')
        if response == "Unknown Command":
            raise RuntimeError(response)
        else:
            return response

    def read_count(self, channel: str):
        """
        Reads the count value from the specified channel.

        Args:
            channel (str): The channel from which to read the count value. Can take values of "CH1", "CH2", or "COINCIDENCE".

        Returns:
            int: The count value from the specified channel.
        
        Raises:
            ValueError: If an invalid channel is specified.
        """
        if channel.upper()=="CH1":
            self.send_command("COUN:C1?")
        elif channel.upper()=="CH2":
            self.send_command("COUN:C2?")
        elif channel.upper()=="COINCIDENCE":
            self.send_command("COUN:CO?")
        else:
            raise ValueError(channel + "is an invalid channel")
        
        return int(self.read_response())

    def append_counts_to_csv(self, filename: str):
        """
        Appends the count values to the specified CSV file.

        Args:
            filename (str): The name of the CSV file to append the count values to.

        Returns:
            None
        """
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