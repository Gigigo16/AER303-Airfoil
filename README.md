# AER303 Airfoil Lab

Data and Post-processing code for AER303 Airfoil lab. Created November 23rd 2023.

## File Structure

The file structure for this repository is structured as follows:

* **Data**
  * Contains all raw data files gathered during lab.
* **Results**
  * Contains all processed output data. These files are overwritten each time the processing script is ran.
* **Src**
  * Contains source code for data processer

## Dependancies

The code in this respository has the following depedancies:

- [Python 3.8+](https://www.python.org/) --> Version 3.11 recommended
- [Numpy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Scipi](https://scipy.org/)
- [Pandas](https://pandas.pydata.org/)

## How to Replicate Results:

In order to replicate results seen in lab report the following steps must be taken:

1. **Run Data Filtering Script (filter.m)**
2. **Run Uncertainty Calculations (errorcalc.py)**
   
⋅⋅⋅[WARNING] -> May take over an hour to compute uncertainties for all 456 values (38 (# of ports) * 12 * (# of AoAs)) as each  point requires the calculation of a convolution accross 90,090 points and a numerical integration accross a large range of values leading to a very large runtime. It is not recommended to run this and instead utilize the values in "/data/CSV/dX_xx.csv" (which we have calculated). However, if desired, results can be verified by deleting the existing CSVs and running this script.
4. **Run main processing script (main.py)**

Results should now be present in results folder.

## Authors

- [Rodrigo Salazar](https://www.github.com/Gigigo16)
- [Felix Hlady](https://www.github.com/FelHy66)
- [Sahil Swali]()
- [Sritejas Murugan](https://github.com/smurugan23)
