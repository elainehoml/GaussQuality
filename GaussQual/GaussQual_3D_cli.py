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
    # parser.add_argument(
    #     "-f",
    #     "--file_prefix",
    #     dest="prefix",
    #     help="Name of the image, e.g., <img_dir>/<prefix>/<prefix>_0000.tif"    
    # )
    parser.add_argument(
        "-n",
        "--n_components",
        dest="n_components",
        type=int,
        help="Number of Gaussian components to fit"
    )

    return parser