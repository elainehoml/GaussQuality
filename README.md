# GaussQual
GAUSSian mixture model image QUALity assessment

Fits Gaussian Mixture Models to 2D and 3D greyscale X-ray micro-computed tomography images, to estimate Gaussian properties of material grey values.

---

# Example Usage for CLI

## 2D image

In a terminal (Git Bash or similar), run:
This code fits `n_comp` number of Gaussian components to the 2D image specified.

``` 
python GaussQual_2D.py -f "example_image.tif" -n <n_comp>
```

To threshold the grey values, add the following arguments:

``` 
-t <min_grey_value> <max_grey_value>
```

### Plots

To plot the histogram, add `-p`.

To change the histogram labels to match the constituent materials, use the argument `--material_names` and add the material names in ascending order of their mean grey values ($\mu$). For example,

``` 
--material_names ["<mat_1>",  "<mat_2>", ... , "<mat_n>"]
```

To show the image side-by-side with the histogram, use `-pp`. For both the histogram and the side-by-side image, use `ppp`.

To show the plot, use `--show_plots`.

### Calculate SNR and CNR

To calculate SNR and CNR, specify `-c` and the index of the Gaussians you would like to calculate SNR and CNR for. For example, if there are 3 Gaussians where the background is Gaussian 0 (lowest grey value), and the feature is Gaussian 2 (highest grey value), 

```
-c --background 0 --feature 1
```

`--background` and `--feature` can also take more than 1 argument, but the same number of values must be specified for both.

### Save results

To save just the fitted results, use `-s`.
To save the fitted results and the plots, use `-ss`.

---

For more information, use the help function:
``` 
python GaussQual_2D.py -h
```
