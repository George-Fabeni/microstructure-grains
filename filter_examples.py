from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
img = Image.open("imagens/grains.jpeg")
img.show()
img2=np.asarray(img)
print(img.format)
print(img2.shape)

########################
# Abrindo com matplotlib
########################

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img3 = mpimg.imread("imagens/grains.jpeg")
print(img3)
print(img3.shape)
plt.imshow(img3)


######################
# abrindo com skimage
######################

from skimage import io
image = io.imread("imagens/grains.jpeg")
io.imshow(image)
print(image)

####################
# Abrir com CV2
####################

import cv2
import numpy as np

img5 = cv2.imread("imagens/google.png", 1)
#cv2.imshow("teste", img5)
img6 = img5[300:400,100:400]
cv2.imshow("cortada", img6)
print(img6.shape)
print(img6[45:50,45:50])
cv2.waitKey(0)
cv2.destroyAllWindows()

###################
# Abrir com skimage
###################
import cv2
from skimage import io
from skimage.filters import roberts, sobel, scharr, prewitt
from skimage.feature import canny
from matplotlib import pyplot as plt
img = io.imread("imagens/grains.jpeg", as_gray=True)
roberts2 = roberts(img)
sobel2 = sobel(img)
scharr2 = scharr(img)
prewitt2 = prewitt(img)
canny2 = canny(img, sigma=3)

fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey= True, figsize=(8,8))
ax = axes.ravel()
ax[0].imshow(roberts2, cmap=plt.cm.gray)
ax[0].set_title("original")

ax[1].imshow(sobel2, cmap=plt.cm.gray)
ax[1].set_title("robert")

ax[2].imshow(scharr2, cmap=plt.cm.gray)
ax[2].set_title("scharr")

ax[3].imshow(prewitt2, cmap=plt.cm.gray)
ax[3].set_title("sprewitt")

for a in ax:
    a.axis("off")
    
plt.tight_layout()
plt.show()

#cv2.imshow("teste", edge)
#cv2.imshow("teste", sobel2)
#cv2.imshow("teste", scharr2)
#cv2.imshow("teste", prewitt2)
cv2.waitKey(0)
cv2.destroyAllWindows()
plt.imshow(edge)




