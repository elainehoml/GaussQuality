import os
import sys
import numpy as np
import pytest
import skimage.io

test_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(test_dir)
gaussquality_dir = os.path.join(base_dir, "gaussquality")
sys.path.append(gaussquality_dir)
img_dir = os.path.join(test_dir, "example_images", "3D_")

import gaussquality_io

def test_get_img_list():
    """
    Checks correct number of images are added to list and they are sorted
    """
    img_list = gaussquality_io.get_img_list(img_dir)
    assert (len(img_list) == 50) and (img_list[0].endswith("00.tif"))


def test_get_img_filepath():
    """
    Gets a filename for a random slice between 10-50 and checks it's correct
    """
    slice_no = np.random.randint(10, 50)
    img_filepath = gaussquality_io.get_img_filepath(img_dir, slice_no)
    assert img_filepath.endswith("{}.tif".format(slice_no))


def test_mask_img():
    """
    Tests that mask is applied correctly
    """
    # Create test image with square in the center random%
    mask_pct = np.random.randint(0, 100)
    test_img = np.zeros([100, 100])
    minimum = int(50 - (mask_pct/2))
    maximum = int(50 + (mask_pct/2))
    test_img[minimum:maximum, minimum:maximum].fill(1)

    # Apply mask
    masked_img = gaussquality_io.mask_img(test_img, mask_pct)

    # If mask is in centre, mean of masked_img = 1
    # If mask is correct shape, masked size / original = mask pct
    assert (np.mean(masked_img) == 1) and (masked_img.shape[0]/test_img.shape[0] == pytest.approx(mask_pct/100, rel=0.05)) and (masked_img.shape[1]/test_img.shape[1] == pytest.approx(mask_pct/100, rel=0.05))


def test_load_img():
    """
    Tests that an example image is loaded correctly
    """
    # Random slice of test dataset
    slice_no = np.random.randint(10, 50)
    img_filepath = gaussquality_io.get_img_filepath(img_dir, slice_no) 
    img_load = skimage.io.imread(img_filepath) # load with different library

    # Load image, full size
    img_test = gaussquality_io.load_img(img_filepath)
    masked_size = (int(img_test.shape[0]*0.2), int(img_test.shape[1]*0.2))

    # Load image, masked to 20%
    masked_img = gaussquality_io.load_img(img_filepath, mask_percentage=20)

    # Get a 20x20 patch of images to compare
    patch_img_load = img_load[40:60, 200:220]
    patch_img_test = img_test[40:60, 200:220]

    assert (masked_size == masked_img.shape) and (patch_img_load == pytest.approx(patch_img_test, rel=1e-1))