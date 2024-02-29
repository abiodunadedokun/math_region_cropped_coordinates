#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os
import cv2

def crop_and_save(input_image_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # reading image
    image = cv2.imread(input_image_path)

    # converting to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # applying canny edge detection
    edged = cv2.Canny(gray, 10, 250)

    # finding contours
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    idx = 0
    cropped_coordinates = []

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w > 50 and h > 50:
            idx += 1
            new_img = image[y:y + h, x:x + w]
            cropped_coordinates.append((x, y, x + w, y + h))

            # Save the cropped image
            cv2.imwrite(os.path.join(output_folder, f"cropped_{idx}.png"), new_img)

            # Remove the cropped region from the input image
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)

    # Save the modified input image without cropped regions
    cv2.imwrite(os.path.join(output_folder, "input_without_cropped.png"), image)

    # Save the coordinates of the cropped regions in a single text file
    with open(os.path.join(output_folder, "cropped_coordinates.txt"), "w") as f:
        for idx, coord in enumerate(cropped_coordinates, start=1):
            f.write(f"cropped_{idx}:{coord}\n")

    print('Objects Cropped Successfully!')
    print('Results saved in:', output_folder)

# Example usage
input_image_path = 'equ_imgbb.jpg'
output_folder = 'output_folder'
crop_and_save(input_image_path, output_folder)


# In[ ]:




