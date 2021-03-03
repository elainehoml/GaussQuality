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

    if args.plots > 0:
        if (not args.show_plots) and (args.save_results<2):
            print("Warning, plots have been generated but not shown or saved. \
                Specify --show_plots to show plots or -ss to save plots")

    if (args.plots == 1) or (args.plots == 3):
        if args.material_names is not None:
            material_names=args.material_names
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
    
        if args.show_plots:
            plt.show()

        if args.save_results>=2:
            plt.savefig(os.path.splitext(args.img_filepath)[0] + "_histogram.png")
            print("Histogram saved to {}_histogram.png".format(os.path.splitext(args.img_filepath)[0]))
    
    if (args.plots == 2) or (args.plots == 3):
        if args.material_names is not None:
            material_names=args.material_names
            if len(material_names) != len(mu):
                raise ValueError("Incorrect number of material names passed, should be {}".format(len(mu)))
            GaussQual_visuals.plot_img_and_histo(
                args.img_filepath,
                args.mask_percentage,
                [mu, sigma, phi],
                threshold=args.threshold,
                material_names=args.material_names
            )

        else:
            GaussQual_visuals.plot_img_and_histo(
                args.img_filepath, args.mask_percentage, [mu, sigma, phi], args.threshold
            )

        if args.show_plots:
            plt.show()
        
        if args.save_results>=2:
            plt.savefig(os.path.splitext(args.img_filepath)[0] + "_img_and_histogram.png")
            print("Image and histogram side-by-side saved to {}_img_and_histogram.png".format(
                os.path.splitext(args.img_filepath)[0]
            ))

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
        print("Results saved to {}_GMM_results.json".format(os.path.splitext(args.img_filepath)[0]))

if __name__ == "__main__":
    main()
