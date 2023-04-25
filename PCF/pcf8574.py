class PCF8574:
    def __init__(self, i2c, address=0x20):
        self._i2c = i2c
        self._address = address
        self._port = bytearray(1)
        if i2c.scan().count(address) == 0:
            raise OSError('PCF8574 not found at I2C address {:#x}'.format(address))

    @property
    def port(self):
        self._read()
        return self._port[0]

    @port.setter
    def port(self, value):
        self._port[0] = value & 0xff
        self._write()

    def pin(self, pin, value=None):
        pin = self.validate_pin(pin)
        if value is None:
            self._read()
            return (self._port[0] >> pin) & 1
        else:
            if value:
                self._port[0] |= (1 << (pin))
            else:
                self._port[0] &= ~(1 << (pin))
            self._write()

    def toggle(self, pin):
        pin = self.validate_pin(pin)
        self._port[0] ^= (1 << (pin))
        self._write()

    def validate_pin(self, pin):
        # pin valid range 0..7
        if not 0 <= pin <= 7:
            raise ValueError('Invalid pin {}. Use 0-7.'.format(pin))
        return pin

    def _read(self):
        self._i2c.readfrom_into(self._address, self._port)

    def _write(self):
        self._i2c.writeto(self._address, self._port)