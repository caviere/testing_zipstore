# testing_zipstore

This repository has scripts done for the zarr project [Testing the support and interoperability of Zarr ZipStore](https://www.outreachy.org/outreachy-december-2022-internship-round/) by [me](https://www.outreachy.org/alums/2022-12/) for Outreachy December 2022 cohort

# Outline

* [Used real world data to test the support across various Zarr implementations](https://github.com/caviere/testing_zipstore/blob/main/real%20%20world%20data/main.py)
* [Created a MNIST Dataset script](https://github.com/caviere/testing_zipstore/blob/main/py/example.py)
* [Created a benchmark script that reads and writes Zarr arrays using directory, zip and fsspec stores](https://github.com/caviere/testing_zipstore/blob/main/benchmark/main.py)
* [Created a script that benchmarks the timings it takes to fetch data from a zipstore, LRU cache and in memory store using uniform and zipfian distributions](https://github.com/caviere/testing_zipstore/tree/main/cache)

# Support and Interoperability of Zarr Zipstore

This [script](https://github.com/caviere/testing_zipstore/blob/main/real%20%20world%20data/main.py) shows how the following implementations work with the zipstore. Here's a simple rundown: 

| Implementation | Support for Read | Support for Write |
| -------------- | ----------------| ------------------ |
| [Zarr-python](https://zarr.readthedocs.io/en/stable/index.html) | Yes | Yes|
| [Xarray](https://docs.xarray.dev/en/stable/) | Yes | Yes|
| [Netcdf4](https://docs.unidata.ucar.edu/netcdf-c/current/) | No | No |
| [Gdal](https://gdal.org/) | Yes | No |
| [H5py](https://docs.h5py.org/en/stable/) | No | No |
| [Fsspec](https://filesystem-spec.readthedocs.io/en/latest/) | Yes | Yes |

To read in detail about the work done and my time in outreachy, please visit [my website](https://caviere.github.io/) and have a read. Cheers!
