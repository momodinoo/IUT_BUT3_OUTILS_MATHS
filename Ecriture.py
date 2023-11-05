from Func import stegano

# On demande le message qui sera dans l'image
message = input("Entrez le message à cacher dans l'image : ")
print("Le message est : " + message)

# On demande le nom de la future image
imgname = input("Entrez le nom de l'image qui contiendra le message : ")
# On regarde si l'extension .png est là, sinon on la rajoute
if ".png" not in imgname:
    imgname += ".png"
print("Le nom de votre image sera : " + imgname)

try:
    stegano("image.png", message, imgname)
except:
    print('\033[91m' + "Le message n'a pas été codé correctement")
    exit()