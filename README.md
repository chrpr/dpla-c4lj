# Metadata Analytics, Visualization, and Optimization

This repo contains parser code and an iPython notebook that accompany my recent code4lib journal article, [Metadata Analytics, Visualization, and Optimization: Experiments in statistical analysis of the Digital Public Library of America (DPLA)](http://journal.code4lib.org/articles/11752). There are two parts to this repository:

* [parsers](./parsers) contains code to parse DPLA json into field count csvs in both long and wide formats; code to extract the words from each DPLA record by field; and code to merge the field counts csv with output of google anlytics, harvested using [Pyganalytics](https://github.com/chrpr/pyganalytics)
* [notebooks](./notebooks) contains a single iPython notebook that tracks the text of the _Machine Learning and Predictive Analytics_ and _Additional Evaluation Metrics and Ensembles of Trees_ sections of the article. The narrative of these two sections is reproduced, interspersed with scikit learn code and output for running the various machine learning techniques. 

If you'd like to reproduce these results, and are affiliated with a DPLA hub, please get in touch with me about acquiring data. 

If you have any other questions or comments, please feel free to contact me either here, via [email](mailto:corey.harper@gmail.com), or on [twitter](https://twitter.com/chrpr).

