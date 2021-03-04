from argparse import ArgumentParser


def GaussQual3D_parser():
    parser = ArgumentParser(
        description="Assess quality of 3D greyscale images with Gaussian Mixture Models"
    )
    parser.add_argument(
        "-d",
        "--img_dir",
        dest="img_dir",
        help="Path to the directory of the image sequence, e.g., \
            <img_dir>/<prefix>/<prefix>_0000.tif"
    )
    parser.add_argument(
        "-n",
        "--n_components",
        dest="n_components",
        type=int,
        help="Number of Gaussian components to fit"
    )
    parser.add_argument(
        "-z",
        "--z_percentage",
        dest="z_percentage",
        help="Percentage of stack to use in z",
        type=float,
        default=70
    )
    parser.add_argument(
        "-r",
        "--n_runs",
        dest="n_runs",
        help="Number of slices to analyse",
        type=int,
        default=10
    )
    parser.add_argument(
        "--mask_percentage",
        dest="mask_percentage",
        type=float,
        default=100.,
        help="Percentage of image to use in x-y"
    )
    parser.add_argument(
        "-t",
        "--threshold",
        nargs=2,
        default=None,
        type=float,
        help="Min and Max grey values to consider, optional. Default uses entire range."
    )
    parser.add_argument(
        "-p",
        "--plots",
        dest="plots",
        action="store_true",
        help="Plot slice variation. To plot histogram and others please use GaussQual_2D."    
    )
    parser.add_argument(
        "--material_names",
        dest="material_names",
        default=None,
        nargs="*",
        help="List of material names in ascending order of grey value mu"
    )
    parser.add_argument(
        "--show_plots",
        dest="show_plots",
        action="store_true",
        help="Show plots in interactive window"
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