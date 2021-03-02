from argparse import (
    ArgumentParser,
    ArgumentDefaultsHelpFormatter
)


def GaussQual_parser():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-s",
        "--single-image",
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
        "--mu_init",
        dest="mu_init",
        type=list,
        default=None,
        help="Initial guesses of mu, optional. Default is None."
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
        "--plot_histo",
        dest="plot_histo",
        action="store_true",
        help="Show histogram"
    )
    parser.add_argument(
        "--material_names",
        dest="material_names",
        default=None,
        help="List of material names in ascending order of grey value mu, input as a single string separated by spaces e.g. `Air Tissue Wax`"
    )

    return parser
