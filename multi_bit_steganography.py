from math import ceil
from PIL import Image
from file_functions import *

def text_to_binary(text):
    """convert to binary (ASCII → Binary)"""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_string):
    """Convert a binary string to text"""
    chars = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def multi_bit_lsb_steganography(message_path, img_path, bit_depth, step_size):
    # convert to binary
    message = read_file(message_path)
    binary_message = text_to_binary(message)
    message_length = len(binary_message)

    # upload img
    img = Image.open(img_path)
    pixels = list(img.getdata())

    # Keep the message length as the first 8 bits
    binary_length = format(message_length, '08b')
    full_binary = binary_length + binary_message

    if len(full_binary) > len(pixels) * ceil(3 / step_size) * bit_depth:
        raise ValueError("The message is too long to fit into the image.")

    # Insert the message into pixels
    new_pixels = []
    binary_index = 0
    mask = (1 << bit_depth) - 1

    for pixel in pixels:
        new_pixel = list(pixel)  # Convert a tuple to a list
        for channel in range(0, 3, step_size):
            if binary_index < len(full_binary):
                new_pixel[channel] = (new_pixel[channel] & ~mask) | int(full_binary[binary_index:binary_index + bit_depth], 2)
                binary_index += bit_depth
        new_pixels.append(tuple(new_pixel))

    # Save the new image
    img.putdata(new_pixels)
    output_image_path = f"{img_path.rsplit('.', 1)[0]}.png"
    img.save(output_image_path)
    print(f"Message successfully hiding inside: {output_image_path}!")

def multi_bit_lsb_steganography_extraction(img_path, bit_depth, step_size):
    # Loading the image and checking that the format is correct
    img = Image.open(img_path).convert("RGB")  # Converting the image to RGB
    pixels = list(img.getdata())

    mask = (1 << bit_depth) - 1

    channels = list(range(0, 3, step_size))

    binary_length = ''.join(
        bin(pixels[i // len(channels)][channels[i % len(channels)]] & mask)[2:].zfill(bit_depth)
        for i in range(ceil(8 / bit_depth)))[:8]
    message_length = int(binary_length, 2)

    binary_message = ''.join(
            bin(pixels[i // len(channels)][channels[i % len(channels)]] & mask)[2:].zfill(bit_depth)
            for i in range(ceil(message_length / bit_depth)))[8:message_length]

    extracted_text = binary_to_text(binary_message)
    write_result_file(img_path, extracted_text, False)
