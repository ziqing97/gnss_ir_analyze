import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import numpy as np
import matplotlib.image as mpimg

# we need to define the color bar min and max range
h_plot = np.array([1,5])

# generate the colorbar 
norm = matplotlib.colors.Normalize(vmin=min(h_plot),vmax=max(h_plot), clip=True)  # normalization
mapper = cm.ScalarMappable(norm=norm, cmap='jet')   # jet as the colorbar style
h_color = np.array([(mapper.to_rgba(v)) for v in h_plot])  # generate colorbar

# read and show the image
image1 = mpimg.imread('test.jfif')
plt.imshow(image1)

# a dirty trick: to show the colorbar, I plot 2 points in the left top angle, one for color_min and one for color_max
# you can try to plot these 2 points somewhere where the color is right so nobody should detect
plt.scatter([1,1],[2,2],c=h_plot,cmap='jet')

# show colorbar
plt.colorbar()