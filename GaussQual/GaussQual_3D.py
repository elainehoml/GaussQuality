import os
from datetime import date

import GaussQual_io
import GaussQual_fitting
import GaussQual_visuals
import GaussQual_calc
from GaussQual_3D_cli import GaussQual3D_parser


def main():
    args = GaussQual3D_parser().parse_args()

    if args.n_components is None:
        raise ValueError("Please specify number of Gaussians to fit")

    fitted_results, iter_results = GaussQual_fitting.run_GMM_fit(
        args.img_dir,
        args.n_components,
        z_percentage=args.z_percentage,
        n_runs=args.n_runs,
        mask_percentage=args.mask_percentage,
        threshold=args.threshold
    )

if __name__ == "__main__":
    main()