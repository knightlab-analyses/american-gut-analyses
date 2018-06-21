# Analysis Notebooks and Code for The American Gut Project

`ipynb` contains executable Jupyter notebooks.

`ipynb/env` describe the conda and run enviroments associated with these notebooks.

`non-ipynb` contains analyses performed outside of Jupyter notebooks.

# Manuscript

The [manuscript](http://msystems.asm.org/content/3/3/e00031-18) associated with this repository is open access and published under mSystems. If code from this repository or data from the American Gut are used, please consider citing this manuscript.

# Data access

Data for the American Gut Project can be accessed in a few ways and are described in brief below. This is a living project, so these datasets will continue to grow with the exception of the fixed datasets. The fixed datasets correspond to what was used for the manuscript.

* all sequence and metadata are in EBI under the project [PRJEB11419](https://www.ebi.ac.uk/ena/data/view/PRJEB11419). This dataset is not fixed.
* all sequence, metadata and processed summaries can be obtained from [Qiita](https://qiita.ucsd.edu) under study ID 10317. This dataset is not fixed. 
* the 16S and metadata can be obtained by querying [`redbiom`](https://github.com/biocore/redbiom) using `qiita_study_id==10317`. This dataset is not fixed.
* the 16S data in BIOM-Format and metadata used in the manuscript from the public anonymous [microbio.me](ftp://ftp.microbio.me/AmericanGut/manuscript-package/) FTP. This dataset is fixed and will not change.

The metabolomics datasets are housed in [GNPS[(http://gnps.ucsd.edu/). The datasets listed below are fixed. Additional metabolomics data from the American Gut will be available in GNPS in the future.

* the antibiotic [subset](http://gnps.ucsd.edu/ProteoSAFe/status.jsp?task=9bd16822c8d448f59a03e6cc8f017f43)
* the number of types of plants [subset](http://gnps.ucsd.edu/ProteoSAFe/status.jsp?task=d26ae082b1154f73ac050796fcaa6bda)
* the cell culture [supernatant](https://gnps.ucsd.edu/ProteoSAFe/status.jsp?task=23f0f5e5c70f4163b445de71d086d186)
* the co-networked fecal [samples](https://gnps.ucsd.edu/ProteoSAFe/status.jsp?task=adcfbba9b4ca448f8b2133559b16d954)
