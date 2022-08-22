from PIL import Image
from os.path import join as osjoin, dirname

height = 100
width = 100

cadr_x_start = 0
cadr_y_start = 0

step = width * height * 2

with open('C:/Users/artif/OneDrive/Рабочий стол/fl_displey.hex', 'rb') as fp:
    hex_list = fp.read()
    
hex_list = ['{:02X}'.format(b) for b in hex_list]

def twosComplement_hex(hexval):
    bits = 16
    val = int(hexval, bits)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val

img = Image.new('RGB', (240, 240))

index = 0xb0000

while True:

    for y in range(0, height):

        for x in range(0, width):

            a = twosComplement_hex(hex_list[index])
            b = twosComplement_hex(hex_list[index + 1])

            img.putpixel((x,y), (b & 248, 36 * (b & 7) + (a & 192) // 8, 4 * (a & 63)))
            index += 2

    width += 2
    height += 2
    
    print(width)

    index = 0xb0000

    img.show()
