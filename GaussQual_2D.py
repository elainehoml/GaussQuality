import matplotlib.pyplot as plt

import GaussQual_io
import GaussQual_fitting
import GaussQual_visuals
from GaussQual_2D_cli import GaussQual_parser


def main():
    args = GaussQual_parser().parse_args()
    
    img_filepath = args.img_filepath
    img = GaussQual_io.load_img(
        img_filepath,
        mask_percentage=args.mask_percentage
    )
    mu, sigma, phi = GaussQual_fitting.fit_GMM(
        img,
        n_components=args.n_components,
        mu_init=args.mu_init,
        threshold=args.threshold
    )
    if args.plot_histo:
        if args.material_names is not None:
            GaussQual_visuals.plot_GMM(
                img,
                mu,
                sigma,
                phi,
                threshold=args.threshold,
                material_names=args.material_names.split(" "))
        else:
            GaussQual_visuals.plot_GMM(
                img, mu, sigma, phi, threshold=args.threshold
            )
        plt.show()


if __name__ == "__main__":
    main()
