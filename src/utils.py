import numpy as np

plaintext_len_bit_size = 14


def int_to_bin(number: int, length=8) -> str:
    b = bin(number)[2:]
    return ('0' * (-len(b) % length)) + b


def bin_to_int(number: str) -> int:
    return int(number, base=2)


def lsb_encrypt(I, plaintext: str):
    image_shape = I.shape[0:2]
    B = np.ravel(I[:, :, 0])
    plaintext_len_bin = int_to_bin(len(plaintext), length=plaintext_len_bit_size)

    # adding length bits to the image
    for i in range(plaintext_len_bit_size):
        pixel_bin = int_to_bin(B[i])
        pixel_bin = pixel_bin[0:7] + plaintext_len_bin[i]
        B[i] = bin_to_int(pixel_bin)

    # creating bit stream
    stream = []
    for letter in plaintext:
        letter_bin = int_to_bin(ord(letter))
        for bit in letter_bin:
            stream.append(bit)

    # adding the message to the Blue bit stream
    counter = plaintext_len_bit_size
    for bit in stream:
        pixel_bin = int_to_bin(B[counter])
        pixel_bin = pixel_bin[0:7] + bit
        B[counter] = bin_to_int(pixel_bin)
        counter += 1

    B = B.reshape(image_shape)

    # Adding the Blue layer back to the Image
    I[:, :, 0] = B
    return I


def lsb_decrypt(I) -> str:
    # extracting the blue layer and unraveling it
    B = I[:, :, 0]
    B = np.ravel(B)
    plaintext_len_bin = ''
    for i in range(plaintext_len_bit_size):
        plaintext_len_bin += int_to_bin(B[i])[7]

    plaintext_len = bin_to_int(plaintext_len_bin)

    # creating the bit stream from the plaintext_len
    stream = []
    for i in range(plaintext_len_bit_size, plaintext_len_bit_size + 8 * plaintext_len):
        pixel = B[i]
        pixel_bin = int_to_bin(pixel)
        pixel_bit = pixel_bin[7]
        stream.append(pixel_bit)

    # creating plaintext from bit stream
    plaintext = ''
    for i in range(plaintext_len):
        byte = ''.join(stream[8 * i: 8 * i + 8])
        letter = bin_to_int(byte)
        plaintext += chr(letter)

    return plaintext
