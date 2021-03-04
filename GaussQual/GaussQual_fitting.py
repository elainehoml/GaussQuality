# -*- coding: utf-8 -*-
""" Gaussian mixture model fitting for greyscale images: Fitting

Created on Mon Jan 25 15:36:11 2021

@author: elainehoml
"""

import os
import time
import numpy as np
import sklearn.mixture

from GaussQual_io import *


def fit_GMM(img, n_components, mu_init=None, threshold=None):
    """
    Fits Gaussian mixture model to `img` grey values, and return fitted
    Gaussian properties.

    Parameters
    ----------
    img : array-like
        2-D array containing image grey values.
    n_components : int
        Number of Gaussian components to fit to grey value distribution.
        Usually `n_components` = number of materials in the specimen image.
    mu_init : list, optional
        List of initial mean values to use. The default is None.
    threshold : tuple, optional
        (Min, Max) grey value to consider. The default is None.

    Returns
    -------
    mu_fitted : array-like, len=n_components
        Fitted mean of Gaussian components.
    sigma_fitted : array-like, len=n_components
        Fitted standard deviation of Gaussian components.
    phi_fitted : array-like, len=n_components
        Fitted weights of Gaussian components.

    """
    start_time = time.time()

    # Create an instance of GaussianMixture
    GMM_model = sklearn.mixture.GaussianMixture(n_components, random_state=3)

    # Optional initialisation
    if mu_init is not None:
        means_init = np.array(mu_init).reshape((n_components, 1))
        GMM_model.set_params(means_init=means_init)

    # Apply a threshold to ignore values outside this (min, max)
    if threshold is not None:
        img = np.array(list(filter(lambda x: x >= threshold[0], img.flatten())))
        img = np.array(list(filter(lambda x: x <= threshold[1], img)))
    print("Image grey value range = {}-{}".format(
        min(img.flatten()), max(img.flatten())))
    # Fit 1D array of image grey values
    GMM_model.fit(img.reshape(-1, 1))

    # Unpack results
    mu_fitted = GMM_model.means_.flatten()                       # means
    sigma_fitted = np.sqrt(GMM_model.covariances_).flatten()     # stdev
    phi_fitted = GMM_model.weights_.flatten()                    # weights

    # Sort in ascending order of means
    sort_ind = np.argsort(mu_fitted)
    mu_fitted = mu_fitted[sort_ind]
    sigma_fitted = sigma_fitted[sort_ind]
    phi_fitted = phi_fitted[sort_ind]

    print("Time elapsed in s: {}".format(time.time()-start_time))
    print("Means = {}, Stdev = {}, Weights = {}".format(mu_fitted,
                                                        sigma_fitted,
                                                        phi_fitted))
    return mu_fitted, sigma_fitted, phi_fitted


def run_GMM_fit(img_dir, prefix, n_components, z_percentage=70,
                n_runs=30, mask_percentage=70, threshold=None):
    """
    Fit Gaussian mixture models to 2-D images in a 3-D image sequence.

    Parameters
    ----------
    img_dir : str, path-like
        Directory to image.
    prefix : str
        Name of the image.
    n_components : int
        Number of Gaussian components to fit to grey value distribution.
        Usually `n_components` = number of materials in the specimen image.
    z_percentage : float, optional
        Percentage of stack to consider in the z-direction
        Images will be taken evenly over this `z_percentage` centred in the
        central slice. Spacing between images is
        `z_percentage`/100 * `number_of_slices` / `n_runs`. The default is 70.
    n_runs : int, optional
        Number of images to consider from the 3-D sequence. The default is 30.
    mask_percentage : float
        Percentage of the image to consider, as a rectangle centred on `img`.
        Ranges from 0-100.
    threshold : tuple, optional
        (Min, Max) grey value to consider. The default is None.

    Returns
    -------
    fitted_results : list
        List containing fitted Gaussian properties `mu`, `sigma` and `phi`
        averaged across the stack.
    iter_results : list
        List containing dicts of fitted Gaussian properties for each 2-D image
        considered.

    """

    # get number of slices
    nslices = get_nslices(img_dir)

    # generate slice numbers to load, starting from centre and moving outwards
    central_slice = int(nslices/2)
    z_range = int(nslices * z_percentage/100)
    z_step = int(z_range/n_runs)
    run_slices = [central_slice]
    counter = 1
    while len(run_slices) < n_runs:
        run_slices.append(central_slice + counter * z_step)
        run_slices.append(central_slice - counter * z_step)
        counter += 1

    # Initialise empty dict to hold intermediate values of mu, sigma and phi
    mus = {}
    sigmas = {}
    phis = {}

    # Fit GMMs to slices in run_slices
    for run in range(n_runs):
        print("\nRun {}, Slice {}".format(run+1, run_slices[run]))
        # load single slice of image
        img_filepath = get_img_filepath(img_dir, run_slices[run] - 1)
        img = load_img(img_filepath, mask_percentage=mask_percentage)

        # fit GMM and get fitted parameters (mu, sigma, phi)
        if threshold is not None:
            mu_fitted, sigma_fitted, phi_fitted = fit_GMM(img,
                                                          n_components,
                                                          threshold=threshold)
        else:
            mu_fitted, sigma_fitted, phi_fitted = fit_GMM(img, n_components)

        mus[run_slices[run]] = mu_fitted
        sigmas[run_slices[run]] = sigma_fitted
        phis[run_slices[run]] = phi_fitted

        if run == n_runs-1:
            # calculate mean values across stack
            mu_mean = []
            sigma_mean = []
            phi_mean = []
            for material in range(len(mu_fitted)):
                temp_mu = []
                temp_sigma = []
                temp_phi = []
                for run in range(len(mus)):
                    temp_mu.append(mus[run_slices[run]][material])
                    temp_sigma.append(sigmas[run_slices[run]][material])
                    temp_phi.append(phis[run_slices[run]][material])
                mu_mean.append(np.mean(temp_mu))
                sigma_mean.append(np.mean(temp_sigma))
                phi_mean.append(np.mean(temp_phi))

            # return mean values when n_runs is reached
            return [mu_mean, sigma_mean, phi_mean], [mus, sigmas, phis]
