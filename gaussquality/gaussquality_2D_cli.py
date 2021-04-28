# from argparse import ArgumentParser
import argparse

def gaussquality_parser():
    parser = argparse.ArgumentParser(
        description="Assess quality of 2D greyscale images with Gaussian Mixture Models"
    )
    parser.add_argument(
        "-f",
        "--img_filepath",
        dest="img_filepath",
        type=str,
        help="Path to the single image to be analysed"
    )
    parser.add_argument(
        "--mask_percentage",
        dest="mask_percentage",
        type=float,
        default=100.,
        help="Percentage of image to use in x-y"
    )
    parser.add_argument(
        "-n",
        "--n_components",
        dest="n_components",
        type=int,
        help="Number of Gaussian components to fit"
    )
    parser.add_argument(
        "-t",
        "--threshold",
        dest="threshold",
        type=float,
        nargs=2,
        default=None,
        help="Min and Max grey values to consider, optional. Default uses entire range."
    )
    parser.add_argument(
        "-p",
        "--plots",
        dest="plots",
        default=0,
        action="count",
        help="Plot nothing (0) \
              Plot histogram alone (1), \
              Plot image and histogram side-by-side (2) \
              Plot both (3)"
    )
    parser.add_argument(
        "--show_plots",
        dest="show_plots",
        action="store_true",
        help="Show plots"
    )
    parser.add_argument(
        "--material_names",
        dest="material_names",
        default=None,
        nargs="*",
        help="List of material names in ascending order of grey value mu"
    )
    parser.add_argument(
        "-c",
        "--calc",
        dest="calculate",
        action="store_true",
        help="Calculate SNR and CNR"
    )
    parser.add_argument(
        "--background",
        dest="background",
        type=int,
        nargs="*",
        help="Index of background Gaussian, e.g. 0 is the Gaussian with lowest mean grey value, \
            can specify more than one."    
    )
    parser.add_argument(
        "--feature",
        dest="feature",
        type=int,
        nargs="*",
        help="Index of feature Gaussian, e.g. 0 is the Gaussian with the lowest mean grey value, \
            can specify more than one."
    )
    parser.add_argument(
        "-s",
        "--save_results",
        dest="save_results",
        action="count",
        default=0,
        help="Save results. Save nothing (0) \
              Save input arguments (1), \
              Save input arguments, fitted results (2), \
              Save input arguments, fitted results, and plots (3)"
    )

    return parser
