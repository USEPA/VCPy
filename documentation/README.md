####################################
VCPy_chemical_assignments.xlsx

-This document houses all of the species-specific data. 
-All of the physiochemical data is from U.S. EPA's Comptox: https://comptox.epa.gov/dashboard/dsstoxdb/batch_search
-This data is used to populate the /input/chemical_assignments.csv files in the VCPy.
-To re-generate much of the data, enter all "OPERA Input" into: https://comptox.epa.gov/dashboard/dsstoxdb/batch_search.
-All other columns have to be calculated. Equations for these calculations are typically included in the individual cells.

####################################
/air_quality/

-This folder houses data related to SOA and O3 potential.

####################################
/vcpy_evaluation

-This folder houses data/scripts related to Fig. 6 and Fig. S6 of Seltzer et al., 2021

####################################
/organic_composition

-This folder houses data/scripts related to organic composition.
-Files in /input are generated using data from /product_composition.

####################################
/population

-This folder is self-explanatory. All data is related to county and state-level popution counts.

####################################
/product_composition

-Of most importance is the *.xlsx file in this folder. This is data from the 2015 Consumer and Commerical Product
 survey from CARB and used to generate the 1st-order product composition profiles for many of the sub-PUCs.
-Data from the pdf documents in this folder are also used to generate several 1st-order product composition profiles.

####################################
/product_usage

-This folder contains the data used to compute the product usage for most sub-PUCs.

####################################
/spatial_allocation

-This folder contains the data use to allocate national-level emission factors to the state and county-level.