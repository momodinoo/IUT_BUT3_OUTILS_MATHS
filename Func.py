from PIL import Image
from cryptography.fernet import Fernet
import random

key = Fernet.generate_key()


def encrypt(msg):
    msg = msg.encode()
    f = Fernet(key)
    encrypted = f.encrypt(msg)
    encrypted = key + encrypted
    return encrypted.decode()


def decode(msg):
    key = msg[0:44].encode()
    f = Fernet(key)
    decrypted = f.decrypt(msg[44:])
    return decrypted.decode()


def stegano(sourceimgname, message, newimgname):
    msg = encrypt(message)
    # on ouvre l'image
    img = Image.open(sourceimgname)
    img = img.convert("RGBA")
    # on récupère les dimensions de l'image
    width, heigth = img.size
    # on sépare l'image en quatre : rouge, vert, bleu, a
    r, g, b, a = img.split()
    # on transforme la partie rouge en liste
    r = list(r.getdata())
    # on calcule la longueur de la chaîne et on la transforme en binaire
    lenmsg = len(msg)
    lenbinmsg = bin(len(msg))[2:].rjust(16, "0")
    # on transforme la chaîne en une liste de 0 et de 1
    ascii = [bin(ord(x))[2:].rjust(8, "0") for x in msg]
    # transformation de la liste en chaîne
    chaine = ''.join(ascii)
    # on code la longueur de la liste dans les 16 premiers pixels rouges
    for j in range(16):
        r[j] = 2 * int(r[j] // 2) + int(lenbinmsg[j])
    # on code la chaîne dans les pixels
    for i in range(8 * lenmsg):
        r[i + 16] = 2 * int(r[i + 16] // 2) + int(chaine[i])

    imagesize = width * heigth
    nbPixelsModifies = (8 * lenmsg) + 16
    nbPixelRestant = imagesize - nbPixelsModifies
    # on remplit aléatoirement les pixel rouge afin de créer un grain général dans l'image
    for k in range(nbPixelRestant):
        r[k + nbPixelsModifies] = 2 * int(r[k + nbPixelsModifies] // 2) + random.randint(0, 1)

    # on recrée l'image rouge
    nr = Image.new("L", (width, heigth))
    nr.putdata(r)
    # fusion des quatres nouvelles images
    imgnew = Image.merge('RGBA', (nr, g, b, a))
    imgnew.save(newimgname)

    if message == get_msg(newimgname):
        print('\033[92m' + "Le message à bien été écrit dans l'image : " + newimgname)
    else:
        raise Exception("Le message n'est pas bon")


def get_msg(name_couv):
    img = Image.open(name_couv)
    r, g, b, a = img.split()
    r = list(r.getdata())

    # lecture de la longueur de la chaine
    p = [str(x % 2) for x in r[0:16]]
    q = "".join(p)
    q = int(q, 2)

    # lecture du message
    n = [str(x % 2) for x in r[16:16 * (q + 1)]]
    b = "".join(n)
    message = ""
    for k in range(0, q):
        l = b[8 * k:8 * k + 8]
        message += chr(int(l, 2))

    message = decode(message)

    return message
