Required data
---

* RDEFT4_20200515.nc: https://nsidc.org/data/RDEFT4/versions/1
* gsfc_25n.msk: ftp://sidads.colorado.edu/pub/DATASETS/brightness-temperatures/polar-stereo/tools/masks/

These data are expected to be in this directory. The paths in the notebook will need to be updated to use data stored elsewhere.


Setting up the environment
---

Use [conda](https://docs.conda.io/en/latest/miniconda.html) to install the dependencies:

```
conda env create -f environment.yml
```


Running the notebook
---

In this directory, run:

```
jupyter lab
```
