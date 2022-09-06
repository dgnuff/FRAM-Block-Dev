# fram block device driver for CircuitPython

class FRAMDev:
    # param: fram adafruit_fram.FRAM_SPI|adafruit_fram.FRAM_I2C: raw bytearray device
    # return: None
    # This could in theory implement a ramdisk by passing in a suitably sized bytearray
    def __init__(self, fram):
        self._fram = fram
        self._sectors = len(fram) // 512

    # return: int:  the count of 512 byte blocks
    # required
    def count(self):
        return self._sectors

    # param: start_block int: first block to read
    # param: buf bytearray: buffer to receive data
    # return: int: 0 for success
    # prerequisite: len(buf) % 512 == 0
    # prerequisite: len(buf) // 512 + start_block <= self._sectors
    # required
    # read enough data to fill the provided buffer, starting from block number start_address
    def readblocks(self, start_block, buf):
        start_address = start_block * 512
        block_count = len(buf) // 512
        start = 0
        end = 512
        for i in range(block_count):
            buf[start:end] = self._fram[start_address + start:start_address + end]
            start = end
            end += 512
        return 0

    # param: start_block int: first block to write
    # param: buf bytearray: buffer of data to write
    # return: int: 0 for success
    # prerequisite: len(buf) % 512 == 0
    # prerequisite: len(buf) // 512 + start_block <= self._sectors
    # required
    # write the buffer of data to the device, starting at block start_block
    def writeblocks(self, start_block, buf):
        start_address = start_block * 512
        block_count = len(buf) // 512
        start = 0
        end = 512
        for i in range(block_count):
            self._fram[start_address + start:start_address + end] = buf[start:end]
            start = end
            end += 512
        return 0

