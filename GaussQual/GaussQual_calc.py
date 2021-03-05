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
        return mu/sigma


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
        return np.abs(mu_a - mu_b) / sigma_b


def calc_snr_stack(iter_results, background_number,
                   feature_number):
    """
    Calculate SNR for each 2-D image with Gaussian Mixture Model fitted
    from a 3-D image sequence

    Parameters
    ----------
    iter_results : list
        List of fitted `mu`, `sigma` and `phi` Gaussian properties.
    background_number : int
        Material number of background material. Materials are numbered in
        ascending order of `mu`.
    feature_number : int
        Material number of feature material. Materials are numbered in
        ascending order of `mu`.

    Returns
    -------
    snrs : dict
        Dict of SNRs. Keys = slice number, values = SNR.

    """
    mus, sigmas, phis = iter_results
    snrs = {}
    for slice_number in list(mus.keys()):
        mu = mus[slice_number][feature_number]
        sigma = sigmas[slice_number][background_number]
        snrs[slice_number] = calc_snr(mu, sigma)
    return snrs


def calc_cnr_stack(iter_results, background_number,
                   feature_number):
    """
    Calculate CNR for each 2-D image with Gaussian Mixture Model fitted
    from a 3-D image sequence

    Parameters
    ----------
    iter_results : list
        List of fitted `mu`, `sigma` and `phi` Gaussian properties.
    background_number : int
        Material number of background material. Materials are numbered in
        ascending order of `mu`.
    feature_number : int
        Material number of feature material. Materials are numbered in
        ascending order of `mu`.

    Returns
    -------
    cnr : dict
        Dict of CNRs. Keys = slice number, values = CNR.

    """
    mus, sigmas, phis = iter_results
    cnrs = {}
    for slice_number in list(mus.keys()):
        mu_a = mus[slice_number][feature_number]
        mu_b = mus[slice_number][background_number]
        sigma_b = sigmas[slice_number][background_number]
        cnrs[slice_number] = calc_cnr(mu_a, mu_b, sigma_b)
    return cnrs
