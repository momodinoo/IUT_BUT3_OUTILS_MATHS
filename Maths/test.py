from PIL import Image
from cryptography.fernet import Fernet

msg = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"
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


def stegano(imgSourcePath, msg, imgOutPath):
    msg = encrypt(msg)
    # on ouvre l'image
    img = Image.open(imgSourcePath)
    img = img.convert("RGBA")
    # on récupère les dimensions de l'image
    width , heigth = img.size
    # on sépare l'image en quatre : rouge, vert, bleu, a
    r , g , b, a = img.split()
    # on transforme la partie rouge en liste
    r = list( r.getdata() )
    # on calcule la longueur de la chaîne et on la transforme en binaire
    longueurChaine = len(msg)
    longueurChaineBinaire = bin( len(msg) )[2:].rjust(16,"0")
    # on transforme la chaîne en une liste de 0 et de 1 
    ascii = [ bin(ord(x))[2:].rjust(8,"0") for x in msg ]
    # transformation de la liste en chaîne
    chaine = ''.join(ascii)
    # on code la longueur de la liste dans les 16 premiers pixels rouges
    for j in range(16):
        r[j] = 2 * int( r[j] // 2 ) + int( longueurChaineBinaire[j] )
    # on code la chaîne dans les pixels
    for i in range(8 * longueurChaine):
        r[i+16] = 2 * int( r[i+16] // 2 ) + int( chaine[i] )
        
    # on recrée l'image rouge
    nr = Image.new("L", (width, heigth))
    nr.putdata(r)
    # fusion des quatres nouvelles images
    imgnew = Image.merge('RGBA', (nr, g, b, a))
    imgnew.save(imgOutPath)

def get_msg(name_couv):
    img = Image.open(name_couv)
    r , g , b, a = img.split()
    r = list( r.getdata() )
    
    # lecture de la longueur de la chaine
    p = [ str(x%2) for x in r[0:16] ]
    q = "".join(p)
    q = int(q,2)
    
    # lecture du message
    n = [ str(x%2) for x in r[16:16*(q+1)] ]
    b = "".join(n)
    message = ""
    for k in range(0,q):
        l = b[8*k:8*k+8]
        message += chr(int(l,2))
    
    message = decode(message)

    if msg == message:
        print('\033[92m' + "le message à bien été décodé et est identique au message initial")
    else:
        print('\033[91m' + "le message n'a pas été décodé correctement car il n'est pas identique au message initial")

    return message



try :
    stegano("image.png", msg, "couv_image.png")
    stegano("image2.png", msg, "couv_image2.png")
    stegano("image3.png", msg, "couv_image3.png")
except:
    print('\033[91m' + "le message n'a pas été codé correctement")
    exit()

try :
    get_msg("couv_image.png")
    get_msg("couv_image2.png")
    get_msg("couv_image3.png")
except:
    print('\033[91m' + "le message n'a pas été décodé correctement")
    exit()

