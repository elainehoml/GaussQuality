import os
import sys
from pytest import approx
import numpy as np

test_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(test_dir)
GaussQual_dir = os.path.join(base_dir, "GaussQual")
sys.path.append(GaussQual_dir)
img_dir = os.path.join(test_dir, "example_images", "3D_")

import GaussQual_fitting

np.random.seed(12)

def create_test_distribution(mu_phantom, sigma_phantom, phi_phantom):
    gauss1 = np.random.normal(
        mu_phantom[0], 
        sigma_phantom[0],
        size=((10,int(phi_phantom[0] * 100)))
    )
    gauss2 = np.random.normal(
        mu_phantom[1],
        sigma_phantom[1],
        size=((10,int(phi_phantom[1] * 100)))
    )
    test_distribution = np.hstack((gauss1, gauss2))
    return test_distribution


def test_fit_GMM():
    """
    Tests that GMMs are fitted correctly to a test distribution
    """
    mu_phantom = [20., 75.]
    sigma_phantom = [5., 20.]
    phi_phantom = [0.2, 0.8]
    test_img = create_test_distribution(mu_phantom, sigma_phantom, phi_phantom)
    mu, sigma, phi = GaussQual_fitting.fit_GMM(
        test_img,
        2
    )
    assert (mu == approx(mu_phantom, rel=0.1)) and (sigma == approx(sigma_phantom, rel=0.1)) and (phi == approx(phi_phantom, rel=0.1))


def test_fit_GMM_threshold():
    """
    Tests that thresholding ignores grey values outside threshold bounds

    This test distribution has one sharp peaks at 5 and a smaller peak at 100. If thresholding is applied correctly, fitting a single peak to the image thresholded < 50 will only pick up the peak at 5, and vice versa for threshold > 50.
    """
    mu_phantom = [5., 100.]
    sigma_phantom = [2., 2.]
    phi_phantom = [0.7, 0.3]

    test_img = create_test_distribution(mu_phantom, sigma_phantom, phi_phantom)
    mu_low, sigma_low, phi_low = GaussQual_fitting.fit_GMM(
        test_img,
        1,
        threshold = (0, 50)
    )
    mu_high, sigma_high, phi_high = GaussQual_fitting.fit_GMM(
        test_img,
        1,
        threshold = (50, 150)
    )
    assert(mu_low[0] == approx(mu_phantom[0], rel=0.05)) and (mu_high[0] == approx(mu_phantom[1], rel=0.05))


def test_z_crop():
    """
    Tests that z-percentage cropping crops to central specified %
    """
    z_percentage = np.random.randint(1, 100)
    fitted_results, iter_results = GaussQual_fitting.run_GMM_fit(
        img_dir,
        3,
        z_percentage=z_percentage,
        n_runs=3    
    )
    slices = list(iter_results[0].keys())
    assert (max(slices) - min(slices) == int(50 * z_percentage/100)) and (min(slices) == int(25 - 0.5 * z_percentage/100 * 50)) and (max(slices) == int(25 + 0.5 * z_percentage/100 * 50))

