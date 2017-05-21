import smbus

DEVICE_ADDRESS = 0x20
DEVICE_REG_IODIR0 = 0x06
DEVICE_REG_IODIR1 = 0x07
DEVICE_REG_GP0 = 0x00
DEVICE_REG_GP1 = 0x01
PORT_ASSIGNMENT = 8 * [DEVICE_REG_GP0] + 2 * [DEVICE_REG_GP1]
PIN_ASSIGNMENT = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01, 0x40, 0x80]


class I2cBus:
    def __init__(self, log):
        self.log = log
        self.I2Cbus = smbus.SMBus(1)
        self.currentPort = {DEVICE_REG_GP0: 0x00, DEVICE_REG_GP1: 0x00}

        try:
            self.I2Cbus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_GP0, 0x00)
            self.I2Cbus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_GP1, 0x00)
            self.I2Cbus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_IODIR0, 0x00)
            self.I2Cbus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_IODIR1, 0x3F)
        except:
            self.log.error('Error while accessing i2c port')
            exit()

    def write(self, valve_nb, state):
        port = PORT_ASSIGNMENT[valve_nb]
        pin = PIN_ASSIGNMENT[valve_nb]
        if state:
            self.currentPort[port] = self.currentPort[port] | pin
        else:
            self.currentPort[port] = self.currentPort[port] & ~pin
        self.I2Cbus.write_byte_data(DEVICE_ADDRESS, port, self.currentPort[port])
        self.I2Cbus.write_byte_data(DEVICE_ADDRESS, port, self.currentPort[port])
