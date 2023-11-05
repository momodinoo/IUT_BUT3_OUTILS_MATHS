import cv2
import numpy as np


def encode_fourier(image_name: str, code: str):
    image = cv2.imread(image_name)
    b, g, r = cv2.split(image)

    # Effectuer la transformée de Fourier 2D
    f_transform_red = np.fft.fft2(r)

    # Préparer le message pour la composante en niveaux de gris
    ord_msg = [float(ord(char)) for char in code]
    ord_msg += [0.0] * (len(f_transform_red) * len(f_transform_red[0]) - len(ord_msg))

    ord_msg = [ord_msg[i:i + len(f_transform_red[0])] for i in range(0, len(ord_msg), len(f_transform_red[0]))]

    # Modifier les composantes fréquentielles pour cacher le message
    f_transform_edited_red = f_transform_red + ord_msg

    # Inverser la transformation de Fourier
    red_edited = np.abs(np.fft.ifft2(f_transform_edited_red)).astype(np.uint8)

    image_ext = image_name.split(".")[-1]
    extension_position = len(image_name) - len(image_ext) - 1
    image_name_edited = image_name[:extension_position] + "_edited." + image_ext

    image_edited = cv2.merge((b, g, red_edited))
    cv2.imwrite(image_name_edited, image_edited)

    return f_transform_red


def decode_fourier(image_name: str, f_transform: np.ndarray):
    image_modifiee = cv2.imread(image_name)

    b, g, r = cv2.split(image_modifiee)

    f_transform_red_modifiee = np.fft.fft2(r)

    print(f_transform_red_modifiee == f_transform)

    message_red = f_transform_red_modifiee - f_transform

    decoded_message = np.real(message_red).flatten()

    decoded_message = [chr(int(e)) for e in decoded_message]

    print(decoded_message)


if __name__ == '__main__':
    re = encode_fourier("image.jpg", "Coucou, je suis un message caché")
    decode_fourier("image_edited.jpg", re)
