# -*- coding: utf-8 -*-
""" Gaussian mixture model fitting for greyscale images: Visualisation

Created on Mon Jan 25 16:41:57 2021

@author: elainehoml
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from GaussQual_io import *


def plot_GMM(img, mu_fitted, sigma_fitted, phi_fitted, plot_title=None,
             threshold=None, material_names=None, c_bin=0.25):
    """
    Plots histogram of grey values with fitted Gaussians overlaid.
    Number of histogram bins depends on bit depth of image, e.g.
    8-bit images have 256 bins, 16-bit images have 256**2 bins.

    Parameters
    ----------
    img : array-like
        2-D array containing image grey values.
    mu_fitted : array-like, len=n_components
        Fitted mean of Gaussian components.
    sigma_fitted : array-like, len=n_components
        Fitted standard deviation of Gaussian components.
    phi_fitted : array-like, len=n_components
        Fitted weights of Gaussian components.
    plot_title : str, optional
        Adds a title to the plot. The default is None.
    threshold : tuple, optional
        (Min, Max) grey value to consider. The default is None.
    material_names : list, optional
	    List containing material names to add to legend. The default is None.
    c_bin : float, optional, range(0,1)
        Constant by which to multiply sqrt(number of pixels) to determine bin size
        0.125-0.25 for size 512^3 - 2048^3

    Returns
    -------
    None.

    """
    if plot_title is not None:
        plt.title(plot_title)
    plt.xlabel("Grey values")
    plt.ylabel("Probability density")

    # Plot image histogram
    img = img.flatten()  # make 1-d

    if threshold is not None:
        img = np.array(list(filter(lambda x: x >= threshold[0], img.flatten())))
        img = np.array(list(filter(lambda x: x <= threshold[1], img)))
        print("Image thresholded to {}".format(threshold))
        plt.xlim(threshold)

    # hist = plt.hist(img,
    #                 bins=256**img.dtype.itemsize,
    #                 density=True,
    #                 histtype="stepfilled",
    #                 label="Grey Values",
    #                 alpha=0.5)

    # nbins calculation from Reiter et al.
    hist = plt.hist(img,
                    bins=int(c_bin*len(img)**0.5),
                    density=True,
                    histtype="stepfilled",
                    label="Grey Values",
                    alpha=0.5)

    # Generate and plot individual fitted Gaussian distributions
    gaussian_xs = np.linspace(0, max(hist[1]))
    gaussian_ys = np.zeros((len(gaussian_xs), len(mu_fitted)))
    for i in range(len(mu_fitted)):
        gaussian_y = norm.pdf(gaussian_xs, mu_fitted[i], sigma_fitted[i])
        gaussian_ys[:, i] = gaussian_y * phi_fitted[i]
        if material_names is None:
            plt.plot(gaussian_xs, gaussian_y * phi_fitted[i], label="Gaussian {}".format(i))
        if material_names is not None:
            plt.plot(gaussian_xs, gaussian_y * phi_fitted[i], label=material_names[i])

    # Calculate and plot sum of fitted distributions
    sum_gaussians = np.sum(gaussian_ys, axis=1)
    plt.plot(gaussian_xs, sum_gaussians, 'k--', label="Sum of Gaussians")

    plt.legend()


# Plot the variation of sigma across slices
def plot_slice_variation(fitted_results, iter_results, material_names=None):
    """
    Plot fitted `mu`, `sigma` and `phi` distributions over the stack slices

    Parameters
    ----------
    fitted_results : list
        List containing fitted Gaussian properties `mu`, `sigma` and `phi`
        averaged across the stack.
    iter_results : list
        List containing fitted Gaussian properties for each 2-D image
        considered.
    material_names : list, default None.
        List containing material names, e.g. "air".

    Returns
    -------
    None.

    """

    mu_fitted, sigma_fitted, phi_fitted = fitted_results
    mus, sigmas, phis = iter_results

    # Plot variation of mu across slices
    plt.figure(figsize=(6,3))

    if material_names is None:
        material_names = ["Gaussian {}".format(i) for i in range(len(mu_fitted))]

    def subplot(plot_no, fitted, means, material_names):
        plt.subplot(1, 3, plot_no + 1)
        ylabels = ["Mu", "Sigma", "Phi"]
        for i in range(len(material_names)):
            slices = list(means.keys())
            plt.plot([np.min(slices), np.max(slices)],
                     [fitted[i], fitted[i]],
                     "--",
                     label=material_names[i] + " Fitted")
            plt.plot(slices,
                     [means[run][i] for run in slices],
                     ".",
                     color=plt.gca().lines[-1].get_color(),
                     label=material_names[i])
        plt.xlabel("Slices")
        plt.ylabel(ylabels[plot_no])
    subplot(0, mu_fitted, mus, material_names)
    subplot(1, sigma_fitted, sigmas, material_names)
    subplot(2, phi_fitted, phis, material_names)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
    plt.tight_layout()


def plot_img_and_histo(img_filepath, mask_percentage,
                       fitted_results, threshold=None, material_names=None):
    """
    Plots imported image and histogram with overlaid fitted Gaussian
    distributions side-by-side.

    Parameters
    ----------
    img_filepath : str, path-like
        Filepath to image
    mask_percentage : float
        Percentage of the image to consider, as a rectangle centred on `img`.
        Ranges from 0-100.
    fitted_results : list
        List containing fitted Gaussian properties `mu`, `sigma` and `phi`
        averaged across the stack.
    threshold : tuple, optional
        (Min, Max) grey value to consider. The default is None.
    material_names : list, optional
	    List containing material names to add to legend. The default is None.
        Materials should be listed in ascending order of mu.

    Returns
    -------
    None.

    """
    
    plt.figure(figsize=(8,4))
    plt.subplot(121)
    img = load_img(img_filepath,
                   mask_percentage=mask_percentage,
                   show_image=True)
    plt.subplot(122)
    mu_fitted, sigma_fitted, phi_fitted = fitted_results
    plot_GMM(img, mu_fitted, sigma_fitted, phi_fitted, threshold=threshold, material_names=material_names)
    plt.tight_layout()


def vis_slices(n_runs, z_percentage, mask_xy, img_dir):
    """ 3D Plot of data considered for GMM
    
    Parameters
    ----------
    n_runs : int
        Number of runs, i.e. number of z-slices considered.
    z_percentage : float, 0-100
        Percentage of stack to consider
    mask_xy : float, 0-100
        Percentage of x-y image to consider
    img_dir : str, path-like
        Directory where image sequence is
        
    Returns
    -------
    None
    """
    
    # Get z
    n_slices = get_nslices(img_dir)
    n_slices_cropped = int(n_slices * z_percentage/100)
    central_slice = int(n_slices/2)
    z_plot = np.linspace(int(central_slice - n_slices_cropped/2), int(central_slice + n_slices_cropped/2), n_runs)

    # Get xy
    slice_filepath = get_img_filepath(img_dir, 1)
    slice1 = load_img(slice_filepath)
    xy_dims = slice1.shape

    masked_x, masked_y = (int(xy_dims[0]*mask_xy/100), int(xy_dims[1]*mask_xy/100))
    central_x, central_y = (int(xy_dims[0]/2), int(xy_dims[1]/2))
    x = np.linspace(int(central_x - masked_x/2), int(central_x + masked_x/2))
    y = np.linspace(int(central_y - masked_y/2), int(central_y + masked_y/2))
    x_surf, y_surf = np.meshgrid(x, y)
    x_wf, y_wf = np.meshgrid(np.array([int(central_x - masked_x/2), int(central_x + masked_x/2)]),
                             np.array([int(central_y - masked_y/2), int(central_y + masked_y/2)]))

    # Plots
    ax = plt.gca(projection='3d')

    # Plot bounding box of image
    x_bb, y_bb = np.meshgrid([0, xy_dims[0]], [0, xy_dims[1]])
    z_bb = np.meshgrid([0, xy_dims[0]], [0, n_slices])[1]
    z_bb = np.meshgrid([0, xy_dims[1]], [0, n_slices])[1]
    ax.plot_wireframe(x_bb, y_bb, np.zeros(x_bb.shape), color="0.5", 
                      label="Whole image", zorder=0)
    ax.plot_wireframe(x_bb, y_bb, np.full(x_bb.shape, n_slices), 
                      color="0.5", zorder=0)
    ax.plot_wireframe(x_bb, np.zeros(x_bb.shape), z_bb, color="0.5", zorder=0)
    ax.plot_wireframe(x_bb, np.full(x_bb.shape, xy_dims[1]), z_bb, 
                      color="0.5", zorder=0)

    # Plot selected slices
    for slices in z_plot:
        ax.plot_surface(x_surf, y_surf, np.full(x_surf.shape, slices), 
                        alpha=0.05, color="b", zorder=10)
        if slices == z_plot[0]:
            ax.plot_wireframe(x_wf, y_wf, np.full(x_wf.shape, slices), 
                              color="b", alpha=0.5, label="Selected slice", zorder=10)
        else:
            ax.plot_wireframe(x_wf, y_wf, np.full(x_wf.shape, slices), 
                              alpha=0.5, color="b", zorder=10)

    ax.set_xlim([0, xy_dims[0]])
    ax.set_ylim([0, xy_dims[1]])
    ax.set_zlim([0, n_slices])

    ax.set_xlabel("x [px]")
    ax.set_ylabel("y [px]")
    ax.set_zlabel("z [px]")

    ax.grid(False)

    ax.set_box_aspect([xy_dims[0], xy_dims[1], n_slices])
    plt.legend()
