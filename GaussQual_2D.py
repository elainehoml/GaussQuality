import os
import matplotlib.pyplot as plt

import GaussQual_io
import GaussQual_fitting
import GaussQual_visuals
import GaussQual_calc
from GaussQual_2D_cli import GaussQual_parser


def main():
    args = GaussQual_parser().parse_args()
    
    img = GaussQual_io.load_img(
        args.img_filepath,
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
            material_names=args.material_names.split(" ")
            if len(material_names) != len(mu):
                raise ValueError("Incorrect number of material names passed, should be {}".format(len(mu)))
            GaussQual_visuals.plot_GMM(
                img,
                mu,
                sigma,
                phi,
                threshold=args.threshold,
                material_names=material_names
            )
        else:
            GaussQual_visuals.plot_GMM(
                img, mu, sigma, phi, threshold=args.threshold
            )
        plt.show()
    if args.calculate:
        # Dicts to hold SNRs and CNRs
        SNRs = {}
        CNRs = {}

        # Tests
        if (args.background is None) or (args.feature is None):
            raise TypeError("Background and feature Gaussians must be specified as integers")
        if len(args.background) != len(args.feature):
            raise ValueError("Same number of background and feature Gaussians required. \
                you have {} background and {} feature".format(
                    len(args.background), len(args.feature)
                ))

        for i in range(len(args.background)):
            if (args.background[i] > len(mu)) or (args.feature[i] > len(mu)):
                raise ValueError("Background and feature must be between 0 and {}".format(len(mu)))
            SNR = GaussQual_calc.calc_snr(
                mu[args.feature[i]],
                sigma[args.background[i]])
            CNR = GaussQual_calc.calc_cnr(
                mu[args.feature[i]],
                mu[args.background[i]],
                sigma[args.background[i]]
            )
            print("SNR is {}, CNR is {}, with background {} and feature {}".format(
                SNR,
                CNR,
                args.background[i],
                args.feature[i]
            ))
            SNRs["{}-{}".format(args.background[i], args.feature[i])] = SNR
            CNRs["{}-{}".format(args.background[i], args.feature[i])] = CNR
    if args.save_results >= 1:
        if args.calculate:
            GaussQual_io.save_GMM_single_results(
                [mu, sigma, phi],
                os.path.dirname(args.img_filepath),
                os.path.splitext(os.path.basename(args.img_filepath))[0],
                SNRs,
                CNRs
            )
        else:
            GaussQual_io.save_GMM_single_results(
                [mu, sigma, phi],
                os.path.dirname(args.img_filepath),
                os.path.splitext(os.path.basename(args.img_filepath))[0]
            )

if __name__ == "__main__":
    main()
