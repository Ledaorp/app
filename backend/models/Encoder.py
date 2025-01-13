import time
from periphery import I2C

class AS5600:
    # Constants for AS5600
    DEVICE_AS5600 = 0x36
    ANGLE_REGISTER = 0x0C  # Register address for angle

    def __init__(self, bus_number="/dev/i2c-1"):
        # Initialize I2C
        self.i2c = I2C(bus_number)

    def ReadRawAngle(self):  # Read angle (0-360 represented as 0-4096)
        # Write the address of the angle register to read from
        write_msg = I2C.Message([self.ANGLE_REGISTER])
        self.i2c.transfer(self.DEVICE_AS5600, [write_msg])
        
        # Prepare a message to read 2 bytes
        read_data = [0, 0]
        read_msg = I2C.Message(read_data, read=True)
        
        # Read the data
        self.i2c.transfer(self.DEVICE_AS5600, [read_msg])
        
        # Combine the two bytes
        angle = (read_msg.data[0] << 8) | read_msg.data[1]
        return angle & 0x0FFF  # Return only the lower 12 bits
    
    def PrintAngle(self):
        print(f'Angle: {self.Angle()} degrees')

    def Angle(self):
        return (self.ReadRawAngle()*360)/4096
    def close(self):
        self.i2c.close()

#Use
'''if __name__ == "__main__":
    encoder = AS5600()
    while True:
        angle = encoder.ReadRawAngle()
        print(f'Angle: {(angle*360)/4096} degrees')
        time.sleep(1)  # Wait for 1 second before the next reading'''