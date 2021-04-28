import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

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
        # Load image directory
        tk.Label(self.root, text="Load an image sequence folder").grid(row=0)
        tk.Button(self.root, text="Open directory", command=self.get_img_dir).grid(row=0, column=1)
    
        # Choose number of components
        self.n_components = tk.IntVar()
        tk.Label(self.root, text="Number of Gaussian components").grid(row=1)
        ttk.Entry(self.root, textvariable=self.n_components).grid(row=1, column=1)

        # Choose z-percentage
        self.z_percentage = tk.DoubleVar(value=70.)
        tk.Label(self.root, text="Percentage of stack to use in z").grid(row=2)
        ttk.Entry(self.root, textvariable=self.z_percentage).grid(row=2, column=1)

        # Choose number of runs
        self.n_runs = tk.IntVar(value=10)
        tk.Label(self.root, text="Number of slices to analyse").grid(row=3)
        ttk.Entry(self.root, textvariable=self.n_runs).grid(row=3, column=1)

        # Choose mask percentage
        self.mask_percentage = tk.DoubleVar(value=100.)
        tk.Label(self.root, text="Percentage of image to use in x-y").grid(row=4)
        ttk.Entry(self.root, textvariable=self.mask_percentage).grid(row=4, column=1)

        # Choose thresholds
        self.threshold_yes_no = tk.BooleanVar(value=False)
        self.thresholds = None
        ttk.Checkbutton(self.root,
                        text="Apply threshold? (Optional)",
                        variable=self.threshold_yes_no,
                        command=self.apply_threshold).grid(row=5)
        self.lower_threshold = tk.DoubleVar()
        self.upper_threshold = tk.DoubleVar()
        tk.Label(self.root, text="Lower threshold (ignore if no thresholding applied").grid(row=6)
        ttk.Entry(self.root, textvariable=self.lower_threshold).grid(row=6, column=1)
        tk.Label(self.root, text="Upper threshold (ignore if no thresholding applied").grid(row=7)
        ttk.Entry(self.root, textvariable=self.upper_threshold).grid(row=7, column=1)

        # Calculate SNR and CNR
        self.background = tk.IntVar()
        tk.Label(self.root, text="Gaussian component number for background").grid(row=8)
        ttk.Entry(self.root, textvariable=self.background).grid(row=8, column=1)
        self.feature = tk.IntVar()
        tk.Label(self.root, text="Gaussian component number for feature").grid(row=9)
        ttk.Entry(self.root, textvariable=self.feature).grid(row=9, column=1)

        # Run button
        tk.Button(self.root, text="Run GaussQuality", command=self.run_gaussquality).grid(row=10)

        # # STDOUT output
        # self.text_box = tk.Text(self.root, wrap='word').grid(row=11)
        # sys.stdout = StdoutRedirector(self.text_box)
    
    def get_img_dir(self):
        self.img_dir = filedialog.askdirectory()
        print("{} loaded".format(self.img_dir, self.n_components.get()))
    

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

root = tk.Tk()
gaussquality_gui(root)
r = redirector()
root.mainloop()