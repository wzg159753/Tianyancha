import PIL
from PIL import Image


img = Image.open('targetImage.png')
img2 = Image.open('bgImage.png')
print(img.size)
print(img2.size)


new_image = Image.new('RGB', (320, 130), 'red')
new_image.paste(img, (0, 0))
new_image.paste(img2, (0, 30))

new_image.show()
