import numpy as np
from skimage import data
import matplotlib as plt
from scipy import signal
from matplotlib.pyplot import imshow, get_cmap
import matplotlib.pyplot as plt
 
def displayTwoBaWImages(img1, img2):
  """ Display two images"""
  _, axes = plt.subplots(ncols=2)
  axes[0].imshow(img1, cmap=plt.get_cmap('gray'))
  axes[1].imshow(img2, cmap=plt.get_cmap('gray'))

def filter_contrast(img):
    """ Take an image and return it with more contrast """
    kernel = np.array([[0,0,0,0,0], 
                    [0,0,-1,0,0], 
                    [0,-1,5,-1,0], 
                    [0,0,-1,0,0], 
                    [0,0,0,0,0]])
    img_filtered = signal.convolve2d(img, 
                              kernel, 
                              boundary='symm', 
                              mode='same')
    return img_filtered

def filter_blur(img):
    """ Take an image and return it blurred"""
    kernel = np.array([[0,0,0,0,0], 
                    [0,1,1,1,0], 
                    [0,1,1,1,0], 
                    [0,1,1,1,0], 
                    [0,0,0,0,0]])
    img_filtered = signal.convolve2d(img, 
                            kernel, 
                            boundary='symm', 
                            mode='same')
    return img_filtered
    

# ========== MAIN ========== #
img = data.camera()
displayTwoBaWImages(img, filter_contrast(img))


# SHOW IMAGES
plt.show()