####################################################################################################
### VCPy.v1.0: Results and description published in Seltzer et al. 2021, ACP
####################################################################################################

####################################################################################################
### VCPy.v1.1a:
    -Updated organic profiles for 11 sub-PUCs to be consistent with results from
     the 2013-2015 CARB Consumer & Commerical Product survey:
	*CP_Detergents_Soaps
	*CP_General_Cleaners
	*PCP_Daily_Use_Products
	*PCP_Short_Use_Products
	*AS_Adhesives_Sealants
	*COAT_Aerosol
	*COAT_Allied
	*PEST_FIFRA
	*PEST_Agricultural
	*Misc_All
	*FL_Fuels_Lighter
    -Product usage for 2017; shipment data from 2017 Economic Census;
     required new NAIPS --> sub-PUC mapping.
####################################################################################################

####################################################################################################
### VCPy.v1.1b:
    -Updated all programs to generate time series of emissions upon execution.
    -Product usage for 2018 added; shipment data from 2018 ASM; required new mapping.
    -Removed Runtime.txt file. All runtime variables now entered in VCPy.main.py.
    -Transformed previous modules, which were exclusively executable statements, into
     function definition files. VCPy.main.py is now the main driver of all executions.
    -Fixed bug in speciated_spatial_allocation.py: allocation based on estimated
     emissions; not organic composition profiles.
####################################################################################################