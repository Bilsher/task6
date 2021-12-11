import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

from skimage.filters import (gaussian, threshold_otsu, 
                             threshold_local, 
                             threshold_yen, 
                             threshold_li)

def lakes_and_bays(image):
	b = ~image
	lb = label(b)
	regs = regionprops(lb)
	count_lakes = 0
	count_bays = 0
	for reg in regs:
		on_bound = False
		for y, x in reg.coords:
			if y == 0 or x == 0 or y == image.shape[0] - 1 or x == image.shape[1] - 1:
				on_bound = True
				break
		if not on_bound:
			count_lakes += 1
		else:
			count_bays += 1
	return count_lakes, count_bays

def has_vline(image):
	lines = np.sum(image, axis=0) // image.shape[0]
	return 1 in lines

def filling_factor(image):
	return np.sum(image) / image.size

def recognize(region):
    	if np.all(region.image):
        		return "-"
    	cl, cb = lakes_and_bays(region.image)
    	if cl == 2:
        		if has_vline(region.image):
        			return "B"
        		else:
        			return "8"
    	if cl == 1:
        		if cb == 2:
        			if region.image[region.image.shape[0]//2, region.image.shape[1]//2] > 0:
        				return "P"
        			else:
        				return "D"
        		elif cb == 3:
        			return "A"
        		else:
        			return "0"
    	if cl == 0:
        		if has_vline(region.image):
        			return "1"
        		if cb == 2:
        			return "/"
        		cut_lakes, cut_cb = lakes_and_bays(region.image[2:-2, 2:-2])
        		if cut_cb == 4:
        			return "X"
        		if cut_cb == 5:
        			cy = region.image.shape[0]//2
        			cx = region.image.shape[1]//2
        			if region.image[cy, cx] > 0:
        				return "*"
        			return "W"
    	return None


image = plt.imread("symbols.png")
binary = np.sum(image,2)
binary[binary > 0] = 1

labeled = label(binary)
print(str(labeled.max()))

regions = regionprops(labeled)

d = {None: 0}
for region in regions:
    symbol = recognize(region)
    if symbol is not None:
        #labeled[region.coords] = 0
        labeled[np.where(labeled == region.label)] = 0
    else:
       print(filling_factor(region))
    if symbol not in d:
        d[symbol] = 0
    d[symbol] += 1

print(d)
print("Prosents of symbols: " + str(round((1. - d[None] / sum(d.values())) * 100, 2)) + "%")

#print(regions[3].area)
#print(lakes_and_bays(regions[72]))

plt.imshow(labeled)
#plt.imshow(regions[3].image, cmap="gray")
plt.show()
