import os
from PIL import Image, ImageDraw

# Create 32x32 image with rounded corners approximation
img = Image.new('RGBA', (32, 32), (15, 42, 68, 255))  # #0F2A44 background
draw = ImageDraw.Draw(img)

# Draw the background with rounded corners (approximate)
draw.rectangle([1, 1, 30, 30], fill=(15, 42, 68, 255), outline=(15, 42, 68, 255))

# Draw lines (stroke #1B7F79)
draw.line([8, 10, 24, 10], fill=(27, 127, 121), width=3)
draw.line([8, 16, 20, 16], fill=(27, 127, 121), width=3)
draw.line([8, 22, 16, 22], fill=(27, 127, 121), width=3)

# Draw circle
draw.ellipse([20, 18, 28, 26], fill=(27, 127, 121))

# Save as ICO
img.save('assets/favicon.ico', format='ICO', sizes=[(32,32), (16,16)])

print("favicon.ico created")