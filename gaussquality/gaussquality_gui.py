import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
import matplotlib.pyplot as plt

import gaussquality_io
import gaussquality_fitting
import gaussquality_calc
import gaussquality_visuals

class gaussquality_gui(tk.Frame):

    def __init__(self, root=None):
        super().__init__(root)
        root.title("GaussQuality: Image Quality Assessment with Gaussian Mixture Models")
        self.root = root
        print("-------- GaussQuality --------")
        self.create_widgets()
    
    def create_widgets(self):
        
        # Headers
        self.logo = tk.PhotoImage(file="gaussquality_logo_smol.pnm")
        ttk.Label(self.root, image=self.logo).grid(row=0, column=0)
        ttk.Label(self.root, text="GaussQuality: Image quality evaluation with Gaussian Mixture Models", font=(None, 15)).grid(row=0, column=1, columnspan=3)
        
        # Load image directory
        ttk.Button(self.root,
                   text="Load an image sequence folder", 
                   command=self.get_img_dir
                   ).grid(row=1, column=0, columnspan=2, sticky="NWES")
        # self.img_dir_label = ttk.Label(self.root,
        #                                text="No directory loaded").grid(row=1, column=1)
    
        # Choose number of components
        self.n_components = tk.IntVar()
        ttk.Label(self.root,
                 text="Number of Gaussian components"
                 ).grid(row=2, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                 textvariable=self.n_components
                 ).grid(row=2, column=2, columnspan=2, sticky="NWES")

        # Choose z-percentage
        self.z_percentage = tk.DoubleVar(value=70.)
        ttk.Label(self.root,
                  text="Percentage of stack to use in z"
                  ).grid(row=3, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                  textvariable=self.z_percentage
                  ).grid(row=3, column=2, columnspan=2, sticky="NWES")

        # Choose number of runs
        self.n_runs = tk.IntVar(value=10)
        ttk.Label(self.root,
                  text="Number of slices to analyse"
                  ).grid(row=4, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                  textvariable=self.n_runs
                  ).grid(row=4, column=2, columnspan=2, sticky="NWES")

        # Choose mask percentage
        self.mask_percentage = tk.DoubleVar(value=100.)
        ttk.Label(self.root,
                  text="Percentage of image to use in x-y"
                  ).grid(row=5, column=0, columnspan=2, sticky="NWES")
        ttk.Entry(self.root,
                  textvariable=self.mask_percentage
                  ).grid(row=5, column=2, columnspan=2, sticky="NWES")

        # Preview
        ttk.Button(self.root,
                   text="Preview", 
                   command=self.preview
                   ).grid(row=6, column=0, columnspan=2, sticky="NWES")

        # # Choose thresholds
        # self.threshold_yes_no = tk.BooleanVar(value=False)
        # self.thresholds = None
        # ttk.Checkbutton(self.root,
        #                 text="Apply threshold? (Optional)",
        #                 variable=self.threshold_yes_no,
        #                 command=self.apply_threshold).grid(row=5)
        # self.lower_threshold = tk.DoubleVar()
        # self.upper_threshold = tk.DoubleVar()
        # tk.Label(self.root, text="Lower threshold (ignore if no thresholding applied").grid(row=6)
        # ttk.Entry(self.root, textvariable=self.lower_threshold).grid(row=6, column=1)
        # tk.Label(self.root, text="Upper threshold (ignore if no thresholding applied").grid(row=7)
        # ttk.Entry(self.root, textvariable=self.upper_threshold).grid(row=7, column=1)

        # # Calculate SNR and CNR
        # self.background = tk.IntVar()
        # tk.Label(self.root, text="Gaussian component number for background").grid(row=8)
        # ttk.Entry(self.root, textvariable=self.background).grid(row=8, column=1)
        # self.feature = tk.IntVar()
        # tk.Label(self.root, text="Gaussian component number for feature").grid(row=9)
        # ttk.Entry(self.root, textvariable=self.feature).grid(row=9, column=1)

        # # Run button
        # tk.Button(self.root, text="Run GaussQuality", command=self.run_gaussquality).grid(row=10)
    
    def get_img_dir(self):
        self.img_dir = filedialog.askdirectory()
        print("{} loaded".format(self.img_dir, self.n_components.get()))
        # self.img_dir_label.configure(text=self.img_dir)
        # self.img_dir_label.update_idletasks()
    
    def preview(self):
        print("Loading preview")
        central_slice = int(0.5*gaussquality_io.get_nslices(self.img_dir))
        img_filepath = gaussquality_io.get_img_filepath(self.img_dir, central_slice)
        plt.figure()
        plt.subplot(121)
        img = gaussquality_io.load_img(img_filepath,
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
        if self.threshold_yes_no.get() == True:
            self.thresholds = (self.lower_threshold.get(), self.upper_threshold.get())
    
    
    def run_gaussquality(self):
        print("Running Gaussquality with...")
        print("Image directory: {}".format(self.img_dir))
        print("Number of components: {}".format(self.n_components.get()))
        print("Number of slices to analyse: {}".format(self.n_runs.get()))
        print("Percentage of stack in z: {}".format(self.z_percentage.get()))
        print("Percentage of image to use in xy: {}".format(self.mask_percentage.get()))
        print("Threshold: {}".format(self.thresholds))
        print("Gaussian component for background: {}".format(self.background.get()))
        print("Gaussian component for feature: {}".format(self.feature.get()))
        gaussquality_fitting.run_GMM_fit(self.img_dir, 
                                         self.n_components.get(),
                                         self.z_percentage.get(),
                                         self.n_runs.get(),
                                         self.mask_percentage.get(),
                                         self.thresholds)


class StdoutRedirector(object):
    def __init__(self, text_area):
        self.text_area = text_area
    def write(self, str):
        self.text_area.insert("end", str)
    def flush(self):
        pass


def redirector(inputStr=""):
    root = tk.Toplevel()
    T = tk.Text(root)
    sys.stdout = StdoutRedirector(T)
    T.pack()
    T.insert("end", "------- GaussQuality Output window --------")
    T.insert("end", inputStr)

root = ThemedTk(theme="black")
gaussquality_gui(root)
r = redirector()
root.mainloop()