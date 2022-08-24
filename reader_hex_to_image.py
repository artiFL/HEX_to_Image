from PIL import Image
from os.path import join as osjoin, dirname

'''
Режим перебора ширины изображения нужен для подбора действующей жирины изображения (выравнивания)
т.к изначальная ширина изображения не известна а баты рассположены последовательно друг за гругом необходимо знать на каком значении заканчивается 1 горизонтальная строка пикселей
в ином случае даже при сдвиге на 1 пиксель изображение ломается и становится нечитаемым

Если исспользуется режим перебора ширины изображения 
значение "width" необходимо поставить меньше переменной "width_end"
'''

start_address = 0x00000                                 #Адресс начала чтения Hex файла

height = 320                                            #Высота получаемого изображения 
width = 400                                              
step_iteration =  1                                     #Шаг итерации ширины
width_end = 480                                         #Ширина получаемого изображения

flag_pars = 1                                           #Флаг метода если равен 0 то скрипт выводит 1 изображение если равен 1 то выводит серию изображений с перебором ширины и высоты изображения 



Path = 'C:/Users/flegler.a/Desktop/fl_displey.hex'      #Указывается путь до читаемого файла (обратить внимание что при указании путей исспользуется '/' вместо '\')

with open(Path, 'rb') as fp:                            #Открывтие файла в bin режиме
    hex_list = fp.read()                                #Чтение всего файла
    
hex_list = ['{:02X}'.format(b) for b in hex_list]       #Преобразование массива байт в список

def twosComplement_hex(hexval):                         #Функия преобразования полученой каши в удобочитаемый вид
    bits = 16
    val = int(hexval, bits)
    if val & (1 << (bits-1)):
        val -= 1 << bits
    return val

img = Image.new('RGB', (width_end, height))                      #создание объекта изображения

index = start_address                                   #задание итерируемого стартового адреса

if flag_pars == 1:
    while True:
        for y in range(0, height):
            for x in range(0, width_end):

                a = twosComplement_hex(hex_list[index])                  #чтение 2х байт для 1го пикселя                   
                b = twosComplement_hex(hex_list[index + 1])

                img.putpixel((x,y), (b & 248, 36 * (b & 7) + (a & 192) // 8, 4 * (a & 63))) #конвертация uint16_t в RGB565 
                index += 2

        width += step_iteration                  

        print(width)

        index = start_address

        img.show()

else:

    for y in range(0, height):

        for x in range(0, width):

            a = twosComplement_hex(hex_list[index])
            b = twosComplement_hex(hex_list[index + 1])

            img.putpixel((x,y), (b & 248, 36 * (b & 7) + (a & 192) // 8, 4 * (a & 63)))
            index += 2

    width += 2
    height += 2

    print(width)

    index = start_address

    img.show()