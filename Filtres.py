from PIL import Image

kernels = {
  'blur': [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
  ],
  'contrast': [
    [0, 0, 0, 0, 0],
    [0, 0, -1, 0, 0],
    [0, -1, 5, -1, 0],
    [0, 0, -1, 0, 0],
    [0, 0, 0, 0, 0],
  ],
  'border': [
    [0, 0, 0],
    [-1, 1, 0],
    [0, 0, 0],
  ]
}

def _convolve(K, M):
  return sum(sum(K[i][j]*M[i][j] for j in range(len(K))) for i in range(len(K)))

def _convolve_pixels(K, pixels, w, h):
  n = len(K)
  m = (n-1)//2
  t = sum(sum(abs(K[i][j]) for j in range(len(K))) for i in range(len(K)))
  t += 1 if t == 0 else t
  new_pixels = []
  for x in range(w*h):
    # Construction de la matrice M
    M = [[0 for _ in range(n)] for __ in range(n)]
    for i in range(-m, m+1, 1):
      for j in range(-m, m+1, 1):
        idx = x+i*w+j
        if (0 <= idx < len(pixels)): # Pas les bords
          M[i][j] = pixels[idx]

    # Modification du pixel
    new_pixels.append(_convolve(K, M) / t)

  return new_pixels

def apply_filter(kernel, img: Image, save_path: str):
  print("Applying filter...")
  img = img.convert('RGBA')
  w, h = img.size
  img_r, img_g, img_b, img_a = img.split()
  r = _convolve_pixels(kernel, list(img_r.getdata()), w, h)
  g = _convolve_pixels(kernel, list(img_g.getdata()), w, h)
  b = _convolve_pixels(kernel, list(img_b.getdata()), w, h)
  img_r.putdata(r)
  img_g.putdata(g)
  img_b.putdata(b)
  new_img = Image.merge('RGBA', (img_r, img_g, img_b, img_a))
  new_img.save(save_path)
  print("DONE")


if __name__ == '__main__':
  from Func import stegano, get_msg

  image = Image.open('image.png')
  apply_filter(kernels['blur'], image, 'image_filtre.png')

  message = 'Ceci est un message caché dans une image avec un filtre'
  try:
    stegano('image_filtre.png', message, 'image_filtre_avec_message.png')
    print(get_msg('image_filtre_avec_message.png'))
  except:
      print('\033[91m' + 'Le message n\'a pas été codé correctement' + '\033[0m')
      exit()
