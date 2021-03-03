# -*- coding: utf-8 -*-
"""
Gaussian mixture model fitting for greyscale images: IO

Created on Mon Jan 25 14:50:04 2021

@author: elainehoml
"""

import os, json
import pandas as pd
import matplotlib.pyplot as plt
from skimage import io


def get_img_filepath(img_dir, prefix, slice_number):
    """
    Get single image filepath for image sequence folders

    e.g. if an image sequence is saved under `img_dir/prefix/prefix0001.tif`,
    this function returns the filepath including the correct number of 0's
    at the beginning of the filename.

    Parameters
    ----------
    img_dir : str, path-like
        Directory to image.
    prefix : str
        Name of the image.
    slice_number : int
        Int between 0 and 10000 which represents slice number.

    Returns
    -------
    str, path-like
        Full filepath to the slice slice_number of the image sequence saved
        as `img_dir/prefix/prefix<slice_number>`.

    """
    if slice_number < 10:
        return os.path.join(img_dir,
                            prefix,
                            "{}000{}.tif".format(prefix, slice_number))
    elif slice_number < 100:
        return os.path.join(img_dir,
                            prefix,
                            "{}00{}.tif".format(prefix, slice_number))
    elif slice_number < 1000:
        return os.path.join(img_dir,
                            prefix,
                            "{}0{}.tif".format(prefix, slice_number))
    elif slice_number < 10000:
        return os.path.join(img_dir,
                            prefix,
                            "{}{}.tif".format(prefix, slice_number))


def get_nslices(img_folder):
    """
    Gets number of slices in an image sequence folder.

    Parameters
    ----------
    img_folder : str, path-like
        Path to folder containing single images.

    Returns
    -------
    int
        Number of images in the sequence. Must ensure that no other files
        exist in the folder besides the images.

    """
    return len(os.listdir(img_folder))


def mask_img(img, mask_percentage):
    """
    Applies a mask in x-y plane to only consider the central `mask-percentage`
    percentage of the image.

    Parameters
    ----------
    img : array-like
        2-D array containing image grey values.
    mask_percentage : float
        Percentage of the image to consider, as a rectangle centred on `img`.
        Ranges from 0-100.

    Returns
    -------
    masked_img : array-like
        Central `mask-percentage` of the 2D image `img`

    """
    if mask_percentage < 0 or mask_percentage > 100:
        raise ValueError("`mask_percentage` must be a percentage between \
                         0 and 100")
    mask_width = int(img.shape[0] * mask_percentage/100)
    mask_height = int(img.shape[1] * mask_percentage/100)
    centre_x, centre_y = (int(img.shape[0]/2), int(img.shape[1]/2))
    x_bounds = (int(centre_x - mask_width/2), int(centre_x + mask_width/2))
    y_bounds = (int(centre_y - mask_height/2), int(centre_y + mask_height/2))
    masked_img = img[x_bounds[0]:x_bounds[1], y_bounds[0]:y_bounds[1]]
    return masked_img


def load_img(img_filepath, show_image=False, mask_percentage=100.):
    """
    Loads image from `img_filepath` and applies a mask with percentage
    `mask_percentage`.

    Parameters
    ----------
    img_filepath : str, path-like
        Filepath to the image to import.
    show_image : bool, optional
        If True, display the image. The default is False.
    mask_percentage : float, optional
        Percentage of the image to import, as a rectangle centred in the x-y
        plane. The default is 100..

    Returns
    -------
    img : array-like
        2-D array representing masked image.

    """
    img = io.imread(img_filepath)
    masked_img = mask_img(img, mask_percentage)
    if show_image is True:
        plt.imshow(masked_img, cmap="gray")
        plt.title("{}\n{}".format(os.path.split(img_filepath)[-1],
                                  masked_img.shape))
    return masked_img


def save_GMM_single_results(fitted_results, img_dir, prefix, SNR=None, CNR=None):
    """
    Saves average fitted Gaussian properties across the stack.

    Parameters
    ----------
    fitted_results : list
        List containing fitted Gaussian properties `mu`, `sigma` and `phi`
        averaged across the stack.
    img_dir : str, path-like
        Directory to image.
    prefix : str
        Name of the image.
    SNR : dict, optional.
        SNR. Default is None.
    CNR : dict, optional.
        CNR. Default is None.

    Returns
    -------
    None.

    """
    save_single_filename = os.path.join(img_dir, prefix + "_GMM_results.json")

    # unpack results
    mu_mean, sigma_mean, phi_mean = fitted_results

    # create dict
    dict_to_write = {}
    for material in range(len(mu_mean)):
        dict_to_write["material_" + str(material)] = []
        dict_to_write["material_" + str(material)].append({
            "mu_mean": mu_mean[material],
            "sigma_mean": sigma_mean[material],
            "phi_mean": phi_mean[material]
        })
    if (SNR is not None) and (CNR is not None):
        dict_to_write["SNR"] = SNR
        dict_to_write["CNR"] = CNR

    with open(save_single_filename, "w") as outfile:
        json.dump(dict_to_write, outfile, indent=4)


def save_GMM_slice_results(iter_results, img_dir, prefix):
    """
    Saves fitted Gaussian properties for each individual 2-D image considered
    from a 3-D image sequence

    Parameters
    ----------
    iter_results : list
        List of fitted `mu`, `sigma` and `phi` Gaussian properties.
    img_dir : str, path-like
        Directory to image.
    prefix : str
        Name of the image.

    Returns
    -------
    None.

    """
    parameters = ["mu", "sigma", "phi"]
    for parameter in range(len(parameters)):
        save_filename = os.path.join(img_dir,
                                     prefix + "_" + parameters[parameter] + "_GMM_slice_results.json")
        pd.DataFrame(iter_results[parameter]).to_json(save_filename, indent=4)
