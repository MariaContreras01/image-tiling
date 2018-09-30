from PIL import Image
from PIL import GifImagePlugin
from PIL import ImageSequence
import glob
import imageio
#imageio.plugins.ffmpeg.download()

import moviepy.editor as mpy
import shutil
import os, os.path

def superimpose(topImage, bottomImage, coordinates):
	topWidth, topHeight = topImage.size
	bottomWidth, bottomHeight = bottomImage.size
	x, y = coordinates
	if(x < 0 or x > bottomWidth or y < 0 or y > bottomHeight):
		print("Error: out of bounds")
		return

	if (topWidth * topHeight) > (bottomWidth * bottomHeight):
		print("Top image is too big")
		return

	rgb_img = topImage.convert('RGB')
	for i in range(topWidth):
		for j in range(topHeight):
			if(i+x >= bottomWidth or j+y >= bottomHeight):
				continue
			#print(i+x, j+y)
			r, g, b = rgb_img.getpixel((i,j))
			bottomImage.putpixel((i+x,j+y), (r, g, b))

def tiling(tilingIm, size=(500, 500)):
	background = Image.new('RGB', size, (255, 192, 203))
    
	tilingWidth, tilingHeight = tilingIm.size
	backgroundWidth, backgroundHeight = background.size 

	m = backgroundWidth // tilingWidth
	n = backgroundHeight // tilingHeight

	for i in range(m + 1):
		for j in range(n + 1):
			x = i * tilingWidth
			y = j * tilingHeight
			superimpose(tilingIm, background, (x, y))
	return background

def tilingGif(gifFrames, size=(500, 500)):
	tiledFrames = []
	for frame in gifFrames:
		print(frame.size)
		tiledFrames.append(tiling(frame, size))
		#tiledFrames[-1].show()
	return tiledFrames

def makeGif(gifName, frames, fps=12):
	if os.path.isdir('./tmp'):
		shutil.rmtree('./tmp')
		os.mkdir('./tmp')
	else:
		os.mkdir('./tmp')
	for i, frame in enumerate(frames):
		frame.save('./tmp/frame_{}.png'.format(i))
	file_list = glob.glob('./tmp/*.png')
	list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0]))
	clip = mpy.ImageSequenceClip(file_list, fps=fps)
	clip.write_gif('{}.gif'.format(gifName), fps=fps)




bitCoinGif = Image.open("spinningBitcoin.gif")
print(bitCoinGif.is_animated)
print("Number of frames:", bitCoinGif.n_frames)

#resizing image
width, height = bitCoinGif.size
print("Width:", width, "height:", height)

basewidth = 50
wpercent = (basewidth / float(width))
hsize = int ((float(height) * float(wpercent)))
#resizedGif = bitCoinGif.resize((basewidth, hsize))
#resizedGif.save('resized_bitgif.gif')
frames = []
#extracting frames from gif
for frame in ImageSequence.Iterator(bitCoinGif):
	frames.append(frame.resize((basewidth, hsize)))

#newImage = Image.new('RGB', (100, 100), color = 'red')
#superimpose(newImage, frames[0], (0,0))
#superimpose(frames[0], newImage, (101, 101))
#superimpose(frames[0], newImage, (75, 75))
#newImage.show();
#tiling(frames[0], (750, 750)).show()

gif_frames=tilingGif(frames, (200, 300))
makeGif('coins', gif_frames, 10)

