from PIL import Image

def _convolve(K, M):
  return sum(sum(K[i][j]*M[i][j] for j in range(len(K))) for i in range(len(K)))

def _idkyet(K, pixels, w, h):
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
  w, h = img.size
  img_r, img_g, img_b = img.split()
  r, g, b = [_idkyet(kernel, list(elt.getdata()), w, h) for elt in img.split()]
  img_r.putdata(r)
  img_g.putdata(g)
  img_b.putdata(b)
  new_img = Image.merge('RGB', (img_r, img_g, img_b))
  new_img.save(save_path)
  print("DONE")



kernel_blur = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]

kernel_contrast = [
    [0, 0, 0, 0, 0],
    [0, 0, -1, 0, 0],
    [0, -1, 5, -1, 0],
    [0, 0, -1, 0, 0],
    [0, 0, 0, 0, 0],
]

kernel_border = [
    [0, 0, 0],
    [-1, 1, 0],
    [0, 0, 0],
]


img = Image.open('paysage.jpg')
apply_filter(kernel_blur, img, 'save.jpg')