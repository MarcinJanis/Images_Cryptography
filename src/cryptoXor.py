import cv2
import numpy as np
import matplotlib.pyplot as plt

def xor(image, key):
    if image.shape != key.shape:
        key = cv2.resize(key, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
    _, key = cv2.threshold(key, 120, 255, cv2.THRESH_BINARY)
    _, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
    output = cv2.bitwise_xor(image, key)
    return output

def encrypt_xor_description():
    txt1 = f"This algorythm use logic xor to encrypt binary image with key image.\n\n"
    txt1 += f"Encryption:\nInput: two binary image - one as an information to encrypt, second as a key\n\n"
    txt1 += f"Decryption:\nInput: two binary image - one as an information to decrypt, second as a key\n\n"
    return '2. Xor \n'+txt1


