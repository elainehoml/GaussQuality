import concurrent.futures
import time
from pathlib import Path

import numpy as np
from sklearn.mixture import GaussianMixture as GM

from gaussquality import gaussquality_io as gq_io


def fit_GMM(
    img: np.ndarray,
    n_components: int,
    mu_init: list = None,
    threshold: tuple = None,
):
    """Fits Gaussian mixture model to `img` grey values, and return fitted
    Gaussian properties.

    Args:
        img (np.ndarray): 2-D array containing image grey values.
        n_components (int): Number of Gaussian components to fit to grey value
            distribution. Usually `n_components` = number of materials in the
            specimen image.
        mu_init (list, optional): List of initial mean values to use.
            Defaults to None.
        threshold (tuple, optional): (Min, Max) grey value to consider.
            Defaults to None.

    Returns:
        mu_fitted (np.ndarray): Fitted mean of Gaussian components.
        sigma_fitted (np.ndarray): Fitted standard deviation of Gaussian
            components.
        phi_fitted (np.ndarray): Fitted weights of Gaussian components.
    """

    start_time = time.time()
    # Create instance of Gaussian Mixture
    GMM_model = GM(n_components, random_state=3)

    # optional initialisation of mus
    if mu_init is not None:
        means_init = np.array(mu_init).reshape((n_components, 1))
        GMM_model.set_params(means_init=means_init)

    # Apply a threshold to ignore values outside (min,max)
    if threshold is not None:
        img = img[(img >= min(threshold)) & (img <= max(threshold))]
    print(f"Image grey value range = {img.min()}-{img.max()}")

    # Fit 1D array of image grey values
    GMM_model.fit(img.reshape(-1,1))

    # Unpack results
    mu_fitted = GMM_model.means_.flatten()
    sigma_fitted = np.sqrt(GMM_model.covariances_).flatten()
    phi_fitted = GMM_model.weights_.flatten()

    # Sort in ascending order of means
    sort_ind = np.argsort(mu_fitted)
    mu_fitted = mu_fitted[sort_ind]
    sigma_fitted = sigma_fitted[sort_ind]
    phi_fitted = phi_fitted[sort_ind]

    print(f"Time elapsed in s: {time.time() - start_time}")
    print(f"Means={mu_fitted}, Stdev={sigma_fitted}, Weights={phi_fitted}")

    return mu_fitted, sigma_fitted, phi_fitted

def run_GMM_fit_img_sequence(
    img_dir: Path,
    n_components: int,
    z_percentage: float = 70,
    n_runs: int = 30,
    mask_percentage: float = 70,
    mu_init: list = None,
    threshold: tuple = None,
):
    """Fit Gaussian mixture models to 2-D images in a 3-D image sequence.

    Args:
        img_dir (Path): Directory where 2D images are stored
        n_components (int): Number of Gaussian components to fit to grey value
            distribution. Usually `n_components` = number of materials in the
            specimen image.
        z_percentage (float, optional): Percentage of stack to consider in the
            z-direction. Images will be taken evenly over this `z_percentage`
            centred in the central slice. Spacing between images is
            `z_percentage`/100 * `number_of_slices` / `n_runs`. Defaults to 70.
        n_runs (int, optional): Number of images to consider from the 3-D
            sequence. Defaults to 30.
        mask_percentage (float, optional): Percentage of the image to consider,
            as a rectangle centred on `img`. Ranges from 0-100. Defaults to 70.
        mu_init (list, optional): Initial mean values to use. Defaults to None.
        threshold (tuple, optional): (Min, Max) grey value to consider.
            Defaults to None.

    Returns:
        fitted_results (list): List containing fitted Gaussian properties `mu`,
            `sigma` and `phi` averaged across the stack.
        iter_results (list): List containing dicts of fitted Gaussian
            properties for each 2-D image considered.
    """
    start = time.time()
    # get number of slices
    nslices = gq_io.get_nslices(img_dir)

    # generate slice numbers to load starting from centre and moving outwards
    central_slice = int(nslices/2)
    z_range = int(nslices * z_percentage/100)
    min_z = int(central_slice - (z_range/2))
    max_z = int(central_slice + (z_range/2))
    run_slices = np.linspace(min_z, max_z, num=n_runs, dtype=int)

    # Initialise empty dict to hold intermediate values of mu, sigma and phi
    mus = {}
    sigmas = {}
    phis = {}

    # Fit GMMs to slices in run_slices
    def run_GMM_one_img(run):
        fpath = gq_io.get_img_filepath(
            img_dir=img_dir,
            index=run_slices[run]-1
        )
        img = gq_io.load_img(
            img_filepath=fpath,
            mask_percentage=mask_percentage
        )
        mu_fitted, sigma_fitted, phi_fitted = fit_GMM(
            img=img,
            n_components=n_components,
            mu_init=mu_init,
            threshold=threshold
        )
        return run, mu_fitted, sigma_fitted, phi_fitted

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for result in executor.map(run_GMM_one_img, range(n_runs)):
            run, mu, sigma, phi = result
            mus[run_slices[run]] = mu
            sigmas[run_slices[run]] = sigma
            phis[run_slices[run]] = phi

    print(f"Total Time elapsed in s: {time.time() - start}")

    return [mus, sigmas, phis]
