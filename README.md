# GaussQual
GAUSSian mixture model image QUALity assessment

Fits Gaussian Mixture Models to 2D and 3D greyscale X-ray micro-computed tomography images, to estimate Gaussian properties of material grey values.

# Example Usage for CLI

## 2D image

In a terminal (Git Bash or similar), run:
This code fits `n_comp` number of Gaussian components to the 2D image specified.

``` 
python GaussQual_2D.py -s "example_image.tif" -n <n_comp>
```

To threshold the grey values, add the following arguments:

``` 
-t <min_grey_value> <max_grey_value>
```

To show the histogram, add `-p`.

To change the histogram labels to match the constituent materials, use the argument `--material_names` and add the material names in ascending order of their mean grey values ($\mu$) in a single string, separated by spaces. For example,

``` 
--material_names "<mat_1> <mat_2> ... <mat_n>"
```

For more information, use the help function:
``` 
python GaussQual_2D.py -h
```
