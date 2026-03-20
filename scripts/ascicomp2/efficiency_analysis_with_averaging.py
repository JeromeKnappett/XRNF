
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from skimage import io,  exposure, img_as_uint, img_as_float


# # Location of the images
# imageFolder = Path('/user/home/data/19791/Spectra_2022_12_11_corse_changed_wbs_offset/')
# darkFolder = Path('/user/home/data/19791/Spectra_2022_12_11_course_Darkfieldt/')
# Location of the images
imageFolder = Path('/user/home/data/DetectorCom/Spectra_2022_12_11_corse_changed_wbs_offset/')
darkFolder = Path('/user/home/data/DetectorCom/Spectra_2022_12_11_course_Darkfieldt/')

saveImages = False ### CHANGE THIS TO AVOID SAVING NEW IMAGES - added by jk

# Calculate the average image
average_image = io.imread(next(imageFolder.glob("*.tif")))
average_image[:] = 0
img_sum = average_image
n = 500
for img_path in darkFolder.glob("*.tif"):
    image = io.imread(img_path)
    average_image = average_image + (image / n)

#io.imshow(average_image)   
    
    
#io.use_plugin('freeimage')

#average_image = exposure.rescale_intensity(average_image, out_range='float')
#average_image = img_as_uint(average_image)    

# Save the average image to disk
if saveImages:
    io.imsave("/user/home/data/19791/Spectra_2022_12_11_course_Darkfieldt_average_image.tif",  average_image.astype(np.uint16))
else:
    pass
#plt.imshow(average_image)
# Load average image
bg = average_image

# Create a list to store the image sums
sums = []
img_list = []
# Loop through the images
for i in range(1, 1634):
    try:
        image = io.imread(imageFolder / f"Spectra_1_{i}.tif")
        
    except:
        pass
    #img_sum = image + (img_sum/20)
    #img_sum = np.mean(image_sum, axis=0) #fix logic to average 20 minutes
    img_list.append(image)
    # Sum every 20 images
    if i % 20 == 0:
        img_sum = np.mean(img_list,axis=0)
        
        if saveImages:            
            # Save the summed images with subtracted bg to disk
            io.imsave('/user/home/data/19791/Spectra_2022_12_11_corse_changed_wbs_offset/summed/' + str(i) + '.tif',  img_sum.astype(np.uint16))
        
        if i==1240:
            numBins = 50
            #plot the histogram of intensity
            counts,bins = np.histogram(img_sum,bins=numBins)
            print(np.shape(bins))
            fig,ax = plt.subplots(3,1,sharey=True,sharex=True)
#            ax[0].hist(img_sum)
            ax[0].hist(bins[:-1],bins,weights=counts)
            ax[0].set_title('Raw mean image')
            image_test = img_sum
        # Subtract the average image
        img_sum = img_sum - bg
        # set all values less than 3 to 0 
        img_sum[abs(img_sum) < 10] = 0
        
        if i==1240:
            #overplot the histogram of intensity after bg subtraction.
            counts,bins = np.histogram(img_sum,bins=numBins)
            ax[1].hist(bins[:-1],bins,weights=counts)
#            ax[1].hist(img_sum)
            ax[1].set_title('Processed mean image')
            
            counts,bins = np.histogram(bg,bins=numBins)
            ax[2].hist(bins[:-1],bins,weights=counts)
            ax[2].hist(bg)
            ax[2].set_title('Background')
#            ax[2].set_xlim([5000,50000])
            plt.show()
            
            plt.imshow(img_sum,aspect='auto')
            plt.colorbar()
            plt.show()
        
        # normalising image for profile comparison - jk
        norm_img_sum = (img_sum/np.max(img_sum))*65535
        
        if saveImages:            
            # Save the summed images with subtracted bg to disk
            io.imsave('/user/home/data/19791/Spectra_2022_12_11_corse_changed_wbs_offset/processed/' + str(i) + '.tif',  img_sum.astype(np.uint16))
            io.imsave('/user/home/data/19791/Spectra_2022_12_11_corse_changed_wbs_offset/normalised/' + str(i) + '.tif',  norm_img_sum.astype(np.uint16))
        
        sums.append(img_sum)
        img_sum = np.zeros_like(img_sum)
        img_list = []

# Plot the sum intensity of every image sum
intensities = [np.sum(img_sum) for img_sum in sums]
energy_range =  np.arange(90,900,10)
plt.plot(energy_range,intensities)
plt.xlabel("Energy")
plt.ylabel("Intensity")
plt.show()

