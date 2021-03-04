import os
import matplotlib.pyplot as plt
from datetime import date
import json

import GaussQual_io
import GaussQual_fitting
import GaussQual_visuals
import GaussQual_calc
from GaussQual_2D_cli import GaussQual_parser


def main():
    args = GaussQual_parser().parse_args()
    
    if args.n_components is None:
        raise ValueError("Please specify number of Gaussians to fit")

    img_dir = os.path.dirname(args.img_filepath)
    img_name = os.path.splitext(os.path.basename(args.img_filepath))[0]
    
    img = GaussQual_io.load_img(
        args.img_filepath,
        mask_percentage=args.mask_percentage
    )
    print("Imported image {} with mask % {}".format(
        args.img_filepath,
        args.mask_percentage))
    print("Fullsize image size = " + str(
        GaussQual_io.load_img(args.img_filepath).shape
    ))
    print("Imported image size = " + str(img.shape))
    mu, sigma, phi = GaussQual_fitting.fit_GMM(
        img,
        n_components=args.n_components,
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

        if args.save_results >= 2:
            histo_outfile = os.path.join(
                img_dir,
                "results",
                "{}_histogram_{}.png".format(
                    img_name,
                    date.today().strftime("%Y%m%d"))
                )
            plt.savefig(histo_outfile)
            print("Histogram saved to {}".format(histo_outfile))
    
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
        
        if args.save_results >= 2:
            img_histo_outfile = os.path.join(
                img_dir,
                "results",
                "{}_img_and_histogram_{}.png".format(
                    img_name,
                    date.today().strftime("%Y%m%d"))
                )
            plt.savefig(img_histo_outfile)
            print("Image and histogram side-by-side saved to {}".format(img_histo_outfile))

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

        # Save input args
        args_filename = os.path.join(
            img_dir,
            "results",
            "{}_{}_input.json".format(
                img_name,
                date.today().strftime("%Y%m%d")))
        with open(args_filename, "w") as outfile:
                json.dump(vars(args), outfile, indent=4)
        print("Input arguments saved to {}".format(args_filename))
        
        # Save fitted results, SNR and CNR if applicable.
        if args.calculate:
            GaussQual_io.save_GMM_single_results(
                [mu, sigma, phi],
                os.path.dirname(args.img_filepath),
                os.path.splitext(os.path.basename(args.img_filepath))[0] + "_" + date.today().strftime("%Y%m%d"),
                SNRs,
                CNRs
            )
        else:
            GaussQual_io.save_GMM_single_results(
                [mu, sigma, phi],
                os.path.dirname(args.img_filepath),
                os.path.splitext(os.path.basename(args.img_filepath))[0] + "_" + date.today().strftime("%Y%m%d")
            )
        print("Results saved to {}_{}_GMM_results.json".format(
            os.path.splitext(args.img_filepath)[0],
            date.today().strftime("%Y%m%d")))
    
    if (args.save_results >= 2) and (args.plots == 0):
        print("No plots were generated, so no plots were saved. Use `-p` to plot.")

if __name__ == "__main__":
    main()
