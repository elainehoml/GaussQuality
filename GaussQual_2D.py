import matplotlib.pyplot as plt

import GaussQual_io
import GaussQual_fitting
import GaussQual_visuals
import GaussQual_calc
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
    if args.calculate:
        if (args.background is None) or (args.feature is None):
            raise TypeError("Background and feature Gaussians must be specified as integers")
        if (args.background > len(mu)) or (args.feature > len(mu)):
            raise ValueError("Background and feature must be between 0 and {}".format(len(mu)))
        SNR = GaussQual_calc.calc_snr(
            mu[args.feature],
            sigma[args.background])
        CNR = GaussQual_calc.calc_cnr(
            mu[args.feature],
            mu[args.background],
            sigma[args.background]
        )
        print("SNR is {}, CNR is {}, with background {} and feature {}".format(
            SNR,
            CNR,
            args.background,
            args.feature
        ))


if __name__ == "__main__":
    main()
