from Func import get_msg

# On demande le nom de la future image
imgname = input("Entrez le nom de l'image qui contiens le message : ")
# On regarde si l'extension .png est là, sinon on la rajoute
if ".png" not in imgname:
    imgname += ".png"
print("Le nom de votre image est : " + imgname)

try:
    msg = get_msg(imgname)
except:
    print('\033[91m' + "Le message n'a pas été décodé correctement")
    exit()

print("Le message caché est : " + msg)
