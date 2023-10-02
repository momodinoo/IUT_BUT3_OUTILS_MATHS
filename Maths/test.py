from PIL import Image
from cryptography.fernet import Fernet

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


def stegano(imgpath, msg):
    msg = encrypt(msg)
    # on ouvre l'image
    im = Image.open(imgpath)
    im = im.convert("RGBA")
    # on récupère les dimensions de l'image
    w , h = im.size
    # on sépare l'image en quatre : rouge, vert, bleu, a
    r , g , b, a = im.split()
    # on transforme la partie rouge en liste
    r = list( r.getdata() )
    # on calcule la longueur de la chaîne et on la transforme en binaire
    u = len(msg)
    v = bin( len(msg) )[2:].rjust(8,"0")
    # on transforme la chaîne en une liste de 0 et de 1 
    ascii = [ bin(ord(x))[2:].rjust(8,"0") for x in msg ]
    # transformation de la liste en chaîne
    chaine = ''.join(ascii)
    # on code la longueur de la liste dans les 8 premiers pixels rouges
    for j in range(8):
        r[j] = 2 * int( r[j] // 2 ) + int( v[j] )
    # on code la chaîne dans les pixels
    for i in range(8*u):
        r[i+8] = 2 * int( r[i+8] // 2 ) + int( chaine[i] )
        
    # on recrée l'image rouge 
    nr = Image.new("L",(16*w,16*h))
    nr = Image.new("L",(w,h))
    nr.putdata(r)
    # fusion des quatres nouvelles images
    imgnew = Image.merge('RGBA', (nr, g, b, a))
    imgnew.save("/Users/matteo/Python projects/Maths/couv_image.png")

stegano("/Users/matteo/Python projects/Maths/image.png",
        "Bonjour, ceci est un test de stéganographie. Le message est caché dans les pixels rouge.")

def get_msg(name_couv):
    im = Image.open(name_couv)
    r , g , b, a = im.split()
    r = list( r.getdata() )
    
    # lecture de la longueur de la chaine
    p = [ str(x%2) for x in r[0:8] ]
    q = "".join(p)
    q = int(q,2)
    
    # lecture du message
    n = [ str(x%2) for x in r[8:8*(q+1)] ]
    b = "".join(n)
    message = ""
    for k in range(0,q):
        l = b[8*k:8*k+8]
        message += chr(int(l,2))
    
    message = decode(message)
    return message

print(get_msg("/Users/matteo/Python projects/Maths/couv_image.png"))