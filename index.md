This is a tool that fits [Gaussian Mixture Models](https://scikit-learn.org/stable/modules/mixture.html) to grey value distributions from X-ray micro-computed tomography images. This tool was developed as part of a PhD project at the [University of Southampton](https://www.southampton.ac.uk/) in the [3-D X-ray histology team](https://www.southampton.ac.uk/muvis/xrh/xrh-intro.page).

---

## How it works

GaussQuality fits a 1-D Gaussian Mixture Model (GMM) to the grey value distribution of a 2D X-ray micro-computed tomography (&mu;CT) image. The GMM fits a specified number of Gaussian components to the grey value distribution, where each component represents the distribution of grey values for a single material in the specimen. The mean (&mu;), standard deviation (&sigma;), and weight (&phi;) of each Gaussian component are estimated.

* &mu; is the location of the Gaussian along the grey value axis, dependent on X-ray interactions with the material
* &sigma; is its spread which is dependent on heterogeneity of the material and image noise
* &phi; is the proportion of the image taken up by this material

&mu; and &sigma; can be used to calculate signal-to-noise ratio (SNR) and contrast-to-noise ratio (CNR).

&mu;, &sigma;, and &phi; can be estimated for several 2D images in a 3D stack, showing how the image varies in 3D. Only one 2D image is held in memory at once, so images larger than memory can be processed. 3D images must be saved as sequences of 2D images.

---

## Installation

### GUI

Download the .exe for Windows or .app for MacOS. 

Simply double click the executable and the GUI should start. If you have any trouble, try opening the executable in a terminal to debug any errors.

![GaussQuality GUI](gq_gui.JPG)

### Python library

GaussQuality is available on ```conda```. In the terminal:

```
conda activate <myenv>
conda install gaussquality
```

---

## Example usage

See GaussQuality_Example.ipynb for a demo, and explanation of what each parameter controls.

---

## Citation


