# -*- coding: utf-8 -*-
""" Calculates SNR and CNR from grey value means and stdevs

Created on Mon Jan 25 15:50:29 2021

@author: elainehoml
"""

import numpy as np


def calc_snr(mu, sigma):
    """
    Calculate signal-to-noise ratio based on mean `mu` and standard deviation
    `sigma` of a grey value distribution for a material in the image.

    SNR = $\frac{\mu_{feature}}{\sigma_{background}}$

    Parameters
    ----------
    mu : float
        Mean grey value for material which is our feature of interest.
    sigma : float
        Standard deviation of grey values for material representing background.

    Returns
    -------
    float
        SNR.

    """
    if sigma == 0:
        return np.nan
    else:
        return np.mean(mu)/np.mean(sigma)


def calc_cnr(mu_a, mu_b, sigma_b):
    """
    Calculate contrast-to-noise ratio based on mean `mu_a` of feature and
    `mu_b` background material and standard deviation `sigma_b` of the
    background.

    CNR = $\frac{\mu_{feature} - \mu_{background}}{\sigma_{background}}$

    Parameters
    ----------
    mu_a : float
        Mean grey value for material which is our feature of interest.
    mu_b : float
        Mean grey value for material which is our background material.
    sigma_b : float
        Standard deviation of grey values for material representing background.


    Returns
    -------
    float
        CNR.

    """
    if sigma_b == 0:
        return np.nan
    else:
        return (np.mean(mu_a) - np.mean(mu_b)) / np.mean(sigma_b)


def calc_snr_stack(snr, iter_results, prefix, background_number,
                   feature_number):
    """
    Calculate SNR for each 2-D image with Gaussian Mixture Model fitted
    from a 3-D image sequence

    Parameters
    ----------
    snr : dict
        Dict to which SNR values are appended.
        This dict has the structure:
            `snr`[`prefix`] = [`SNR` for each `slice`]
    iter_results : list
        List of fitted `mu`, `sigma` and `phi` Gaussian properties.
    prefix : str
        image prefix, e.g. if the image is "Image01_0000.tif", `prefix` is
        "Image01".
    background_number : int
        Material number of background material. Materials are numbered in
        ascending order of `mu`.
    feature_number : int
        Material number of feature material. Materials are numbered in
        ascending order of `mu`.

    Returns
    -------
    snr : dict
        Dict to which SNR values are appended.

    """
    snr[prefix] = []
    mus, sigmas, phis = iter_results
    for value in range(len(mus)):
        mu = mus[value, feature_number]
        sigma = sigmas[value, background_number]
        snr[prefix].append(calc_snr(mu, sigma))
    return snr


def calc_cnr_stack(cnr, iter_results, prefix, background_number,
                   feature_number):
    """
    Calculate CNR for each 2-D image with Gaussian Mixture Model fitted
    from a 3-D image sequence

    Parameters
    ----------
    cnr : dict
        Dict to which CNR values are appended.
        This dict has the structure:
            `cnr`[`prefix`] = [`CNR` for each `slice`]
    iter_results : list
        List of fitted `mu`, `sigma` and `phi` Gaussian properties.
    prefix : str
        image prefix, e.g. if the image is "Image01_0000.tif", `prefix` is
        "Image01".
    background_number : int
        Material number of background material. Materials are numbered in
        ascending order of `mu`.
    feature_number : int
        Material number of feature material. Materials are numbered in
        ascending order of `mu`.

    Returns
    -------
    cnr : dict
        Dict to which CNR values are appended.

    """
    cnr[prefix] = []
    mus, sigmas, phis = iter_results
    for value in range(len(mus)):
        mu_a = mus[value, feature_number]
        mu_b = mus[value, background_number]
        sigma_b = sigmas[value, background_number]
        cnr[prefix].append(calc_cnr(mu_a, mu_b, sigma_b))
    return cnr
