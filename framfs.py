import busio
import board
import digitalio
import storage
import adafruit_fram
from framdev import FRAMDev

# Adjust this as needed if your SPI bus is not on the usual pins
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# Adjust this as needed for wherever your CS pin is
cs = digitalio.DigitalInOut(board.CS)
# Adjust the max_size parameter to match the size of your fram
fram = adafruit_fram.FRAM_SPI(spi, cs, max_size = 512 * 1024)

# Create the fram block device.
fram_device = FRAMDev(fram)
# Create the filesystem
vfs = storage.VfsFat(fram_device)
# Peek inside the raw fram bytearray, to see if it's already been formatted
if fram[3:11] != b"MSDOS5.0" or fram[43:57] != b"NO NAME    FAT" or fram[510:512] != b"\x55\xAA":
    # And format it if not.  This should format on first use, but on subsequent
    # reloads data in the device will persist.  If you want this to be a true
    # "tempfs", then remove the test above and always execute this line.
    vfs.mkfs(fram_device)

storage.mount(vfs, "/fram")
