import time
from periphery import I2C

class AS5600:
    DEVICE_AS5600 = 0x36
    ANGLE_REGISTER = 0x0C

    def __init__(self, i2c_bus_number="/dev/i2c-1", multiplexer_address=0x70):
        self.i2c = I2C(i2c_bus_number)
        self.multiplexer_address = multiplexer_address

    def set_channel(self, channel):
        if channel < 0 or channel > 7:
            raise ValueError("Channel must be between 0 and 7")
        
        command = 1 << channel  # Set the bit corresponding to the channel
        write_msg = I2C.Message([command])  # Create a message with the command
        
        # Use transfer to send the command to the multiplexer
        self.i2c.transfer(self.multiplexer_address, [write_msg])

    def ReadRawAngle(self):
        write_msg = I2C.Message([self.ANGLE_REGISTER])
        self.i2c.transfer(self.DEVICE_AS5600, [write_msg])
        
        read_data = [0, 0]
        read_msg = I2C.Message(read_data, read=True)
        self.i2c.transfer(self.DEVICE_AS5600, [read_msg])
        
        angle = (read_msg.data[0] << 8) | read_msg.data[1]
        self.close
        return angle & 0x0FFF

    def Angle(self):
        return (self.ReadRawAngle() * 360) / 4096

    def close(self):
        self.i2c.close()

'''Use case
if __name__ == "__main__":
    encoder = AS5600()
    try:
        for channel in range(8):
            encoder.set_channel(channel)
            angle = encoder.ReadRawAngle()
            print(f'Channel {channel}, Angle: {(angle * 360) / 4096:.2f} degrees')
            time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        encoder.close()
'''