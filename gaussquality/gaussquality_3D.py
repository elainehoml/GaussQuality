import os
import json
import datetime
import matplotlib.pyplot as plt

import gaussquality_io
import gaussquality_fitting
import gaussquality_visuals
import gaussquality_calc
import gaussquality_3D_cli

def main():
    args = gaussquality_3D_cli.gaussquality3D_parser().parse_args()
    img_name = os.path.basename(os.path.normpath(args.img_dir))

    if args.n_components is None:
        raise ValueError("Please specify number of Gaussians to fit")

    print("\nImage = {}".format(args.img_dir))
    print("----- Fitting Gaussian -----")
    # Run GMM fitting
    fitted_results, iter_results = gaussquality_fitting.run_GMM_fit(
        args.img_dir,
        args.n_components,
        z_percentage=args.z_percentage,
        n_runs=args.n_runs,
        mask_percentage=args.mask_percentage,
        threshold=args.threshold
    )

    # Plot slice variation
    if args.plots == True:
        print("\n----- Generating plots -----")
        gaussquality_visuals.plot_slice_variation(
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
                    datetime.datetime.now().strftime("%Y%m%d_%H%M"))
            )
            plt.savefig(sv_outfile)
            print("Slice variation plot saved to {}".format(sv_outfile))

    # Calculate SNR and CNR (optional)
    if args.calculate == True:
        print("\n----- Calculating SNR and CNR -----")
        if (args.background is None) or (args.feature is None) or (len(args.background) != len(args.feature)):
            raise ValueError("Please specify equal numbers of background and feature Gaussians.")
        SNRs = {}
        for i in range(len(args.background)):
            SNRs["{}-{}".format(args.background[i], args.feature[i])] = gaussquality_calc.calc_snr_stack(
                iter_results,
                args.background[i],
                args.feature[i]
            )
        print("SNR calculated")

        CNRs = {}
        for i in range(len(args.background)):
            CNRs["{}-{}".format(args.background[i], args.feature[i])] = gaussquality_calc.calc_cnr_stack(
                iter_results,
                args.background[i],
                args.feature[i]
            )
        print("CNR calculated")

        # Print SNR and CNR results
        for i in range(len(args.background)):
            print("Background = {}, Feature = {}".format(
                args.background[i], args.feature[i]
            ))
            snrs = SNRs["{}-{}".format(args.background[i], args.feature[i])]
            cnrs = CNRs["{}-{}".format(args.background[i], args.feature[i])]
            for slice_number in list(snrs.keys()):
                print("Slice number {}: SNR = {}, CNR = {}".format(
                    slice_number,
                    snrs[slice_number],
                    cnrs[slice_number]
                ))

    # Save results    
    if args.save_results >= 1:
        print("\n----- Saving results -----")
        # Save input args
        args_outfile = os.path.join(
            args.img_dir,
            "results",
            "{}_{}_input.json".format(
                img_name,
                datetime.datetime.now().strftime("%Y%m%d_%H%M")))
        with open(args_outfile, "w") as outfile:
                json.dump(vars(args), outfile, indent=4)
        print("Input arguments saved to {}".format(args_outfile))

        # Save fitted results
        gaussquality_io.save_GMM_single_results(
            fitted_results,
            args.img_dir,
            img_name + "_" + datetime.datetime.now().strftime("%Y%m%d_%H%M")
        )
        print("Average stack results saved to {}_{}_GMM_results.json".format(
            args.img_dir,
            datetime.datetime.now().strftime("%Y%m%d_%H%M")))

        # Save iter results
        gaussquality_io.save_GMM_slice_results(
            iter_results,
            args.img_dir,
            img_name
        )

        # Save SNR and CNR
        if args.calculate:
            gaussquality_io.save_SNR_CNR_stack(
                SNRs,
                CNRs,
                args.img_dir,
                img_name
            )
        
    if (args.save_results >= 2) and (args.plots == 0):
        print("No plots were generated, so no plots were saved. Use `-p` to plot.")
        
if __name__ == "__main__":
    main()