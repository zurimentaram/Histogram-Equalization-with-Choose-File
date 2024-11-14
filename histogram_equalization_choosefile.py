import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt

# Membuat dialog file untuk memilih gambar


def choose_file():
    Tk().withdraw()  # Menyembunyikan jendela utama Tkinter
    file_path = askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path


# Memilih file gambar
file_path = choose_file()

# Memeriksa apakah pengguna telah memilih file
if file_path:
    # Membaca gambar dalam mode grayscale
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    # Memeriksa apakah gambar berhasil dimuat
    if image is None:
        print("Error: Gambar tidak dapat dibuka.")
    else:
        # Histogram equalization
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])

        # Menerapkan Histogram Equalization
        cdf = hist.cumsum()  # Menghitung kumulatif distribusi
        cdf_normalized = cdf * hist.max() / cdf.max()

        # Equalize the histogram
        cdf_m = np.ma.masked_equal(cdf, 0)  # Masking nilai nol
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')

        # Menerapkan transformasi ke gambar asli
        image_equalized = cdf[image]

        # Menampilkan gambar asli dan hasil equalization
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.title("Original Image")
        plt.imshow(image, cmap='gray')

        plt.subplot(1, 2, 2)
        plt.title("Equalized Image")
        plt.imshow(image_equalized, cmap='gray')

        plt.show()
else:
    print("Tidak ada file yang dipilih.")
