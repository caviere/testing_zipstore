# testing_zipstore

This repository has scripts done for the zarr project [Testing the support and interoperability of Zarr ZipStore](https://www.outreachy.org/outreachy-december-2022-internship-round/) by me for Outreachy December 2022 cohort

# Outline

* Used real world data to test the support across various Zarr implementations
* Created a MNIST Dataset script
* Created a benchmark script that reads and writes Zarr arrays using directory, zip and fsspec stores
* Created a script that benchmarks the timings it takes to fetch data from a zipstore, LRU cache and in memory store using uniform and zipfian distributions

To read in detail about the work done and my time in outreachy, please visit [my website](https://caviere.github.io/) and have a read. Cheers!
