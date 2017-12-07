

# Data Preprocessing Steps

1. [Vioscreen Report Clean Up]() This notebook takes downloaded Vioscreen CSV files, combines them, and links the survey results to a host subject id and samples.
2. [Metadata clean up and merge](). Combines the sample and prep metadata from [Qiita]() with Vioscreen metadata to build a full mapping file.
3. [Select single fecal sample]() Filters the table to a single fecal sample per participant, based on matches between the SampleID in the full mapping file generated in step 2.
4. [Package Data]() Links the fecal samples selected in step 3 to the sOTU table, alpha diversity, beta diversity, and PICRUSt tables for multiple rarefaction depths.

# Analyses

## Metadata Analysis

* [AG\_World\_Heatmap]() Identifies collection locations of American Gut Samples on a world heatmap
* [Metadata Cross Correlation]() Looks for relationships between metadata categories
* [Demographics]() Compares the demographics in the American Gut data from the United States with US demographic data.
* [social-econ-geo]() Compares the geographic distribution of US American Gut samples with socioeconomic demographics
* [Vioscreen Comparisons]() Looks for Vioscreen covariates that differentiate the people who eat less than 10 types of plants and more than 30.

## Diversity analysis

* [AG\_stool\_temporal dynamics]() Looks at intra indiviudal variation for people with multiple samples.
* [Alpha Diversity Regression]() Performs a multivariate regression comparing alpha diversity to metadata categories with large effect sizes.
* [Country Age and Sex]() Looks at the effect of nationality, age, and biological sex on alpha diversity.
* [Enterotypes]() Evaluates enterotype density in the American Gut dataset

## sOTU based Analyses
* [core-balance-classifier]() Performs balance trees to examine the differences in sOTU abundance due to country and variation in plant consumption.
* [western-nonwestern-balances.ipynb]() Compares the OTU abundances between western and nonwestern populations using balance trees.