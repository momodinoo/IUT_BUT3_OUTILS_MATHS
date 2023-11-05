import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


class SteganoDetector:

    def __init__(self, base_image, second_image):
        self.base_image = base_image
        self.second_image = second_image
        self.base_image_loaded, self.second_image_loaded = self._load_images()

    def _load_images(self):
        return cv2.imread(self.base_image), cv2.imread(self.second_image)

    def _check_size(self):
        if self.base_image_loaded.shape != self.second_image_loaded.shape:
            raise ValueError("Les images n'ont pas la même taille")

    def mse(self):
        self._check_size()

        diff = (self.base_image_loaded.astype(float) - self.second_image_loaded.astype(float)) ** 2
        mse = np.mean(diff)

        return mse

    def psnr(self):
        mse = self.mse()

        if mse == 0:
            return float('inf')

        psnr = 10 * np.log10((255 ** 2) / mse)

        return psnr

    def ssim(self):
        # need scikit-image

        ssim_value = ssim(self.base_image_loaded, self.second_image_loaded, channel_axis=-1)

        return ssim_value
