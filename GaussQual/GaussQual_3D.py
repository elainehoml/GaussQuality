import os
from datetime import datetime
import matplotlib.pyplot as plt

import GaussQual_io
import GaussQual_fitting
import GaussQual_visuals
import GaussQual_calc
from GaussQual_3D_cli import GaussQual3D_parser


def main():
    args = GaussQual3D_parser().parse_args()
    img_name = os.path.basename(os.path.normpath(args.img_dir))

    if args.n_components is None:
        raise ValueError("Please specify number of Gaussians to fit")

    # Run GMM fitting
    fitted_results, iter_results = GaussQual_fitting.run_GMM_fit(
        args.img_dir,
        args.n_components,
        z_percentage=args.z_percentage,
        n_runs=args.n_runs,
        mask_percentage=args.mask_percentage,
        threshold=args.threshold
    )

    # Plot slice variation
    if args.plots == True:
        GaussQual_visuals.plot_slice_variation(
            fitted_results=fitted_results,
            iter_results=iter_results,
            material_names=args.material_names
        )
        if args.show_plots == True:
            plt.show()
        if args.save_results >= 2:
            sv_outfile = os.path.join(
                args.img_dir,
                "results",
                "{}_sv_{}.png".format(
                    img_name,
                    datetime.now().strftime("%Y%m%d_%H%M"))
            )
            plt.savefig(sv_outfile)
            print("Slice variation plot saved to {}".format(sv_outfile))

if __name__ == "__main__":
    main()