# -*- coding: utf-8 -*-
"""
Gaussian mixture model fitting for greyscale images: IO

Created on Mon Jan 25 14:50:04 2021

@author: elainehoml
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import skimage.io
import datetime


def get_img_list(img_dir):
    """
    Gets list of .tiff images in an image sequence folder.

    Parameters
    ----------
    img_dir : str, path-like
        Path to folder containing single images.

    Returns
    -------
    list
        List of image filenames in the folder in ascending order. Only works on .tiff images.

    """
    img_list_unsorted = []
    for f in os.listdir(img_dir):
        if f.lower().endswith((".tif", ".tiff")):
            img_list_unsorted.append(os.path.join(img_dir, f))
    return sorted(img_list_unsorted)

def get_img_filepath(img_dir, index):
    """
    Gets filepath for a specific image in a sequence.

    Parameters
    ----------
    img_dir : str, path-like
        Path to folder containing single images.
    index : int
        Index of image

    Returns
    -------
    str, path-like
        Image filepath for index image in sequence

    """
    img_list = get_img_list(img_dir)
    return img_list[index]


def get_nslices(img_dir):
    """
    Gets number of slices in an image sequence folder.

    Parameters
    ----------
    img_dir : str, path-like
        Path to folder containing single images.

    Returns
    -------
    int
        Number of images in the sequence. Must ensure that no other files
        exist in the folder besides the images.

    """
    return len(get_img_list(img_dir))


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


def load_img(img_filepath, show_image=False, mask_percentage=100., vmin=None, vmax=None):
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
        plane. The default is 100.
    v_min : float, optional, default None
        Minimum grey value to plot
    v_max : float, optional, default None
        Maximum grey value to plot

    Returns
    -------
    img : array-like
        2-D array representing masked image.

    """
    img = skimage.io.imread(img_filepath)
    masked_img = mask_img(img, mask_percentage)
    if show_image is True:
        plt.imshow(masked_img, cmap="gray", vmin=vmin, vmax=vmax)
        plt.title("{}\n{}".format(os.path.split(img_filepath)[-1],
                                  masked_img.shape))
    return masked_img


def save_GMM_single_results(fitted_results, save_dir, prefix, SNR=None, CNR=None):
    """
    Saves average fitted Gaussian properties across the stack.

    Parameters
    ----------
    fitted_results : list
        List containing fitted Gaussian properties `mu`, `sigma` and `phi`
        averaged across the stack.
    save_dir : str, path-like
        Directory to savepath.
    prefix : str
        Prefix to filename
    SNR : dict, optional.
        SNR. Default is None.
    CNR : dict, optional.
        CNR. Default is None.

    Returns
    -------
    None.

    """
    save_single_filename = os.path.join(save_dir, prefix + "_GMM_results.json")

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


def save_GMM_slice_results(iter_results, save_dir, prefix):
    """
    Saves fitted Gaussian properties for each individual 2-D image considered
    from a 3-D image sequence

    Parameters
    ----------
    iter_results : list
        List of fitted `mu`, `sigma` and `phi` Gaussian properties.
    save_dir : str, path-like
        Directory to save results.
    prefix : str
        Prefix to save results filename.

    Returns
    -------
    None.

    """
    parameters = ["mu", "sigma", "phi"]
    for parameter in range(len(parameters)):
        save_filename = os.path.join(save_dir,
                                     "{}_{}_GMM_slice_results.json".format(prefix,
                                     parameters[parameter]))
        pd.DataFrame(iter_results[parameter]).to_json(save_filename, indent=4)


def save_SNR_CNR_stack(SNRs, CNRs, img_dir, img_name):
    dict_to_write = {"SNR": SNRs, "CNR": CNRs}
    snr_cnr_outfile = os.path.join(
        img_dir,
        "results",
        "{}_{}_snr_cnr.json".format(img_name, datetime.datetime.now().strftime("%Y%m%d_%H%M"),))
    with open(snr_cnr_outfile, "w") as outfile:
        json.dump(dict_to_write, outfile, indent=4)
    print("SNR and CNR saved as {}".format(snr_cnr_outfile))
