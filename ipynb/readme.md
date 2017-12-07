

# Data Preprocessing Steps

1. [Vioscreen Report Clean Up](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/VioscreenReportClean.ipynb) This notebook takes downloaded Vioscreen CSV files, combines them, and links the survey results to a host subject id and samples.
2. [Metadata clean up and merge](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/Metadata%20clean%20up%20and%20merge.ipynb). Combines the sample and prep metadata from [Qiita](https://qiita.ucsd.edu/study/description/10317) with Vioscreen metadata to build a full mapping file.
3. [Select single fecal sample](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/Select%20single%20fecal%20sample.ipynb) Filters the table to a single fecal sample per participant, based on matches between the SampleID in the full mapping file generated in step 2.
4. [Package Data](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/Package%20Data.ipynb) Links the fecal samples selected in step 3 to the sOTU table, alpha diversity, beta diversity, and PICRUSt tables for multiple rarefaction depths.

# Analyses

## Metadata Analysis

* [AG\_World\_Heatmap](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/AG_World_Heatmap.ipynb) Identifies collection locations of American Gut Samples on a world heatmap
* [Metadata Cross Correlation](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/Metadata%20cross%20correlation.ipynb) Looks for relationships between metadata categories
* [Demographics](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/Demographics.ipynb) Compares the demographics in the American Gut data from the United States with US demographic data.
* [social-econ-geo](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/social-econ-geo.ipynb) Compares the geographic distribution of US American Gut samples with socioeconomic demographics
* [Vioscreen Comparisons](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/vioscreen_comparisons.ipynb) Looks for Vioscreen covariates that differentiate the people who eat less than 10 types of plants and more than 30.

## Diversity analysis

* [AG\_stool\_temporal dynamics](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/AG_stool_temporal%20dynamics.ipynb) Looks at intra indiviudal variation for people with multiple samples.
* [Alpha Diversity Regression](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/Alpha%20Diversity%20Regression.ipynb) Performs a multivariate regression comparing alpha diversity to metadata categories with large effect sizes.
* [Country Age and Sex](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/Country%20Age%20and%20Sex.ipynb) Looks at the effect of nationality, age, and biological sex on alpha diversity.
* [Enterotypes](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/Enterotypes.ipynb) Evaluates enterotype density in the American Gut dataset

## sOTU based Analyses
* [core-balance-classifier](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/core-balance-classifier.ipynb) Performs balance trees to examine the differences in sOTU abundance due to country and variation in plant consumption.
* [western-nonwestern-balances.ipynb](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/western-nonwestern-balances.ipynb) Compares the OTU abundances between western and nonwestern populations using balance trees.

## Animation
* [animation/Animations (metadata curation)](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/animation/Animations%20(metadata%20curation).ipynb) Combines metadata between American Gut and the other studies used in the animations and standardized fields
* [animations/Animations (processing)](https://github.com/knightlab-analyses/american-gut-analyses/blob/master/ipynb/animation/Animations%20(processing).ipynb) Combines the sOTU tables for the American Gut and other studies used in the meta analysis