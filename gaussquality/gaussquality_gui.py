import os
import sys
import json
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import font
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from gaussquality import gaussquality_io
from gaussquality import gaussquality_fitting
from gaussquality import gaussquality_calc
from gaussquality import gaussquality_visuals

class gaussquality_gui(tk.Frame):

    def __init__(self, root=None):
        super().__init__(root, padx=25, pady=25, bd=25)
        root.title("GaussQuality: Image Quality Assessment with Gaussian Mixture Models")
        self.root = root
        print("-------- GaussQuality --------")
        self.create_widgets()
        self.material_names = None
        self.thresholds = None
        self.snr_cnr_bg = None
        self.snr_cnr_feature = None
    
    def create_widgets(self):
        
        # Headers
        self.logo = tk.PhotoImage(file="logo/gaussquality_logo_greybg_50x50.pnm")
        ttk.Label(self.root, image=self.logo).grid(row=0, column=0, rowspan=2)
        ttk.Label(self.root, 
                  text="GaussQuality: Image quality evaluation with Gaussian Mixture Models",
                  font=("Helvetica", 15)
                  ).grid(row=0, column=1, columnspan=3)
        ttk.Label(self.root,
                  text="University of Southampton, 2021. GNU GPL v3.0",
                  style="TLabel"
                 ).grid(row=1, column=1, columnspan=3)
        
        # Load image directory, set save directory
        ttk.Label(self.root,
                  text="Step 1: Setup",
                  font=("Helvetica", 12, "bold")
                  ).grid(row=2, column=0, columnspan=3, sticky="NWES", ipadx=10, ipady=5)
        ttk.Button(self.root,
                   text="Load an image sequence folder", 
                   command=self.get_img_dir,
                   style="TButton"
                   ).grid(row=3, column=0, columnspan=2, sticky="NWES", ipadx=10, ipady=5)
        ttk.Button(self.root,
                   text="Set save directory", 
                   command=self.set_save_dir,
                   style="TButton"
                   ).grid(row=3, column=2, columnspan=2, sticky="NWES", ipadx=10, ipady=5)

        # Choose number of components
        self.n_components = tk.IntVar()
        ttk.Label(self.root,
                 text="Number of Gaussian components",
                 style="TLabel"
                 ).grid(row=4, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                 textvariable=self.n_components
                 ).grid(row=4, column=2, columnspan=2, sticky="NWS")

        # Choose z-percentage
        self.z_percentage = tk.DoubleVar(value=70.)
        ttk.Label(self.root,
                  text="Percentage of stack to use in z",
                  style="TLabel"
                  ).grid(row=5, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                  textvariable=self.z_percentage
                  ).grid(row=5, column=2, columnspan=2, sticky="NWS")

        # Choose number of runs
        self.n_runs = tk.IntVar(value=10)
        ttk.Label(self.root,
                  text="Number of slices to analyse",
                  style="TLabel"
                  ).grid(row=6, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                  textvariable=self.n_runs
                  ).grid(row=6, column=2, columnspan=2, sticky="NWS")

        # Choose mask percentage
        self.mask_percentage = tk.DoubleVar(value=100.)
        ttk.Label(self.root,
                  text="Percentage of image to use in x-y",
                  style="TLabel"
                  ).grid(row=7, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                  textvariable=self.mask_percentage
                  ).grid(row=7, column=2, columnspan=2, sticky="NWS")

        # Preview
        ttk.Button(self.root,
                   text="Preview", 
                   command=self.preview,
                   style="TButton"
                   ).grid(row=8, column=0, columnspan=2, sticky="NWES", ipadx=10, ipady=5)

        # Choose thresholds
        ttk.Label(self.root,
                  text="Step 2: Set optional parameters",
                  font=("Helvetica", 12, "bold")
                  ).grid(row=9, column=0, columnspan=3, sticky="NWES", ipadx=10, ipady=5)
        self.lower_threshold = tk.DoubleVar()
        self.upper_threshold = tk.DoubleVar()
        ttk.Label(self.root,
                  text="Lower",
                  style="TLabel"
                 ).grid(row=10, column=2, sticky="W")
        ttk.Label(self.root,
                  text="Upper",
                  style="TLabel"
                 ).grid(row=10, column=3, sticky="W")
        ttk.Label(self.root, 
                 text="Grey value thresholds. Ignored if no thresholding applied.",
                 style="TLabel"
                 ).grid(row=11, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                  textvariable=self.lower_threshold
                  ).grid(row=11, column=2, sticky="NWS")
        ttk.Entry(self.root,
                  textvariable=self.upper_threshold
                  ).grid(row=11, column=3, sticky="NWS")
        ttk.Button(self.root,
                   text="Update", 
                   command=self.apply_threshold,
                   style="TButton"
                   ).grid(row=11, column=4, sticky="NWS")

        # Enter a filename to save images
        self.prefix = tk.StringVar(value="Image0")
        ttk.Label(self.root,
                 text="Image name",
                 style="TLabel"
                 ).grid(row=12, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                 textvariable=self.prefix
                 ).grid(row=12, column=2, columnspan=2, sticky="NWS")
        
        # Enter material names for plots
        self.material_names_entry = tk.StringVar()
        ttk.Label(self.root,
                  text="Material names, separated with commas",
                  style="TLabel"
                  ).grid(row=13, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                  textvariable=self.material_names_entry
                  ).grid(row=13, column=2, columnspan=2, sticky="NWS")
        ttk.Button(self.root,
                   text="Update",
                   command=self.add_material_names,
                   style="TButton"
                   ).grid(row=13, column=4, sticky="NWS")

        # Run GaussQuality
        ttk.Button(self.root,
                   text="Run GaussQuality (this could take a while)",
                   command=self.run_gaussquality,
                   style="TButton"
                   ).grid(row=14, column=0, columnspan=2, sticky="NWES", ipadx=10, ipady=5)

        # Plot results
        ttk.Label(self.root,
                  text="Step 3: Plotting",
                  font=("Helvetica", 12, "bold")
                  ).grid(row=15, column=0, columnspan=3, sticky="NWES", ipadx=10, ipady=5)
        ttk.Button(self.root,
                   text="Plot central image and histogram",
                   command=self.plot_image_and_histo,
                   style="TButton"
                   ).grid(row=16, column=0, columnspan=2, sticky="NWS", ipadx=10, ipady=5)
        # self.img_histo_icon = tk.PhotoImage(file="logo/img_and_histo_200x100.pnm")
        # ttk.Label(self.root,
        #           image=self.img_histo_icon
        #          ).grid(row=17, column=0, columnspan=2)
        ttk.Button(self.root,
                   text="Plot slice variation",
                   command=self.plot_slice_variation,
                   style="TButton"
                   ).grid(row=16, column=2, columnspan=2, sticky="NWES", ipadx=10, ipady=5)
        # self.slice_var_icon = tk.PhotoImage(file="logo/slice_var_200x100.pnm")
        # ttk.Label(self.root,
        #           image=self.slice_var_icon
        #           ).grid(row=17, column=2, columnspan=2)
        
        # SNR and CNR calculation
        ttk.Label(self.root,
                  text="Step 4: SNR and CNR Calculation",
                  font=("Helvetica", 12, "bold")
                  ).grid(row=18, column=0, columnspan=3, sticky="NWES", ipadx=10, ipady=5)
        self.background_mat = tk.IntVar()
        self.feature_mat = tk.IntVar()
        ttk.Label(self.root,
                  text="Background Material",
                  style="TLabel"
                 ).grid(row=19, column=2, sticky="W")
        ttk.Label(self.root,
                  text="Feature Material",
                  style="TLabel"
                 ).grid(row=19, column=3, sticky="W")
        ttk.Label(self.root, 
                 text="Material Gaussian numbers for calculating SNR and CNR",
                 style="TLabel"
                 ).grid(row=20, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                  textvariable=self.background_mat
                  ).grid(row=20, column=2, sticky="NWS")
        ttk.Entry(self.root,
                  textvariable=self.feature_mat
                  ).grid(row=20, column=3, sticky="NWS")
        ttk.Button(self.root,
                   text="Update", 
                   command=self.update_materials,
                   style="TButton"
                   ).grid(row=20, column=4, sticky="NWS")
        ttk.Button(self.root,
                   text="Calculate SNR and CNR",
                   command=self.calc_snr_cnr,
                   style="TButton"
                   ).grid(row=21, column=0, columnspan=2, sticky="NWES", ipadx=10, ipady=5)
        

    def get_img_dir(self):
        self.img_dir = filedialog.askdirectory()
        print("{} loaded".format(self.img_dir))
    
    def set_save_dir(self):
        self.save_dir = filedialog.askdirectory()
        print("Save directory is {}".format(self.save_dir))

    
    def preview(self):
        print("Loading preview")
        central_slice = int(0.5*gaussquality_io.get_nslices(self.img_dir))
        self.central_img_filepath = gaussquality_io.get_img_filepath(self.img_dir, central_slice)
        plt.figure()
        plt.subplot(121)
        img = gaussquality_io.load_img(self.central_img_filepath,
                                       show_image=True,
                                       mask_percentage=self.mask_percentage.get())
        plt.title("Slice {}\nMask percentage {}".format(
            central_slice, self.mask_percentage.get()))
        plt.axis('off')
        plt.subplot(122)
        plt.hist(img.flatten(),
                 bins=int(0.45*len(img.flatten())**0.5),
                 density=True,
                 histtype="stepfilled",
                 alpha=0.5)
        plt.xlabel("Grey values")
        plt.ylabel("Probability density")
        plt.tight_layout()
        plt.show()

    def apply_threshold(self):
        self.thresholds = (self.lower_threshold.get(), self.upper_threshold.get())
        print("\nApplying thresholds {}-{}".format(self.thresholds[0], self.thresholds[1]))
    
    
    def run_gaussquality(self):
        if self.img_dir is None:
            raise ValueError("No image sequence selected")
        if self.save_dir is None:
            raise ValueError("No save directory set")
        print("Running Gaussquality with...")
        print("Image directory: {}".format(self.img_dir))
        print("Number of components: {}".format(self.n_components.get()))
        print("Number of slices to analyse: {}".format(self.n_runs.get()))
        print("Percentage of stack in z: {}".format(self.z_percentage.get()))
        print("Percentage of image to use in xy: {}".format(self.mask_percentage.get()))
        print("Threshold: {}".format(self.thresholds))
        self.stack_results, self.slice_results = gaussquality_fitting.run_GMM_fit(
                                            self.img_dir, 
                                            self.n_components.get(),
                                            self.z_percentage.get(),
                                            self.n_runs.get(),
                                            self.mask_percentage.get(),
                                            self.thresholds)
        self.save_results()

    def save_results(self):
        # save input args
        args = {"img_dir": self.img_dir,
                "n_components": self.n_components.get(),
                "n_runs": self.n_runs.get(),
                "z_percentage": self.z_percentage.get(),
                "mask_percentage": self.mask_percentage.get(),
                "threshold": self.thresholds}
        args_outfile = os.path.join(self.save_dir,
                                    "{}_{}_input.json".format(
                                        self.prefix.get(),
                                        datetime.datetime.now().strftime("%Y%m%d_%H%M")
                                    ))
        with open(args_outfile, "w") as outfile:
            json.dump(args, outfile, indent=4)
        print("Input arguments saved to {}".format(args_outfile))

        # save stack results
        self.time_prefix = "{}_{}".format(
            self.prefix.get(),
            datetime.datetime.now().strftime("%Y%m%d_%H%M"))
        gaussquality_io.save_GMM_single_results(
            self.stack_results,
            self.save_dir,
            self.time_prefix
        )
        print("Average stack results saved to {}/{}_GMM_results.json".format(
            self.save_dir,
            self.time_prefix
        ))

        # save slice results
        gaussquality_io.save_GMM_slice_results(
            self.slice_results,
            self.save_dir,
            self.time_prefix)
        print("Slice-by-slice results saved to {}/{}_GMM_slice_results.csv".format(
            self.save_dir,
            self.time_prefix))

    def plot_image_and_histo(self):
        central_slice = int(0.5*gaussquality_io.get_nslices(self.img_dir))
        self.central_img_filepath = gaussquality_io.get_img_filepath(self.img_dir, central_slice)
        gaussquality_visuals.plot_img_and_histo(
            self.central_img_filepath,
            self.mask_percentage.get(),
            self.stack_results,
            self.thresholds,
            self.material_names
        )
        plt.show()

    def plot_slice_variation(self):
        gaussquality_visuals.plot_slice_variation(
            self.stack_results,
            self.slice_results,
            self.material_names
        )
        plt.show()

    def add_material_names(self):
        mat_names = self.material_names_entry.get().split(",")
        self.material_names = mat_names
        print("Material names are {}".format(self.material_names))
    
    def update_materials(self):
        self.snr_cnr_bg = self.background_mat.get()
        self.snr_cnr_feature = self.feature_mat.get()
        print("Background material is Gaussian {}, feature material is Gaussian {}".format(self.snr_cnr_bg, self.snr_cnr_feature))
    
    def calc_snr_cnr(self):
        self.snr = gaussquality_calc.calc_snr_stack(self.slice_results,
                                                    self.snr_cnr_bg, 
                                                    self.snr_cnr_feature)
        self.cnr = gaussquality_calc.calc_cnr_stack(self.slice_results, 
                                                    self.snr_cnr_bg, 
                                                    self.snr_cnr_feature)
        snr_cnr_array = np.zeros((len(self.snr), 3))
        snr_cnr_array[:,0] = list(self.snr.keys())
        snr_cnr_array[:,1] = list(self.snr.values())
        snr_cnr_array[:,2] = list(self.cnr.values())
        snr_cnr_df = pd.DataFrame(snr_cnr_array,
                                  columns=["Slice", "SNR", "CNR"])
        # save snr and cnr
        snr_cnr_outfile = os.path.join(self.save_dir,
                                       "{}_BG{}-F{}_snr_cnr.csv".format(
                                       self.time_prefix,
                                       self.snr_cnr_bg,
                                       self.snr_cnr_feature 
                                       ))
        pd.DataFrame(snr_cnr_df).to_csv(snr_cnr_outfile, index=False)
        print("Slice-by-slice SNR and CNR saved to {}".format(
            snr_cnr_outfile))

class StdoutRedirector(object):
    def __init__(self, text_area):
        self.text_area = text_area
    def write(self, str):
        self.text_area.insert("end", str)
    def flush(self):
        pass


def redirector(inputStr=""):
    root = tk.Toplevel()
    root.configure(background="#424242")
    T = tk.Text(root)
    sys.stdout = StdoutRedirector(T)
    sys.stderr = StdoutRedirector(T)
    T.pack()
    T.insert("end", "------- GaussQuality Log --------\n")
    T.insert("end", inputStr)

root = ThemedTk(theme="black")
style = ttk.Style()
font_label = font.Font(size=11)
style.configure("TLabel", background="#555555", font=font_label)
font_button = font.Font(size=12)
style.configure("TButton", font=font_button)
gaussquality_gui(root)
r = redirector()
root.configure(background="#555555")
root.mainloop()