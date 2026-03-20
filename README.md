# spring-2026-radon-risk-mapping
Team project: spring-2026-radon-risk-mapping

### Team members
1. John Berezney
2. Manimugdha Saikia
3. Huiyao Kuang
4. Emmanuel Asante

### Project overview
This project aims to analyze and predict residential radon risk across Canada using a combination of geological, housing, socioeconomic, climatic, and uranium-related features aggregated at the Forward Sortation Area (FSA) level.  

By integrating radon survey data with census, geological, uranium concentration, and climatic datasets, we aim to better understand which FSAs are more likely to have high radon concentrations and to support risk-informed decision-making.

### Motivation and problem statement
Radon is a naturally occurring radioactive gas and one of the leading causes of lung cancer among non-smokers. Because radon risk is influenced by both geological and built-environment factors, it is important to identify areas with high risk and understand the main contributing features.

In this project, we ask the following question:
"Can we predict high radon risk for each FSA using available census, geological, uranium concentration, and climatic data?"

### Stakeholders
The primary stakeholders for this project include public health agencies, policymakers, and local communities in Canada, who may use this analysis to help prioritize radon testing, mitigation efforts, and risk communication. More broadly, this modeling framework may also be useful to researchers and public health organizations in other countries or regions facing similar radon exposure challenges, particularly where monitoring coverage is limited.

### Dataset
1. Our primary radon data were collected at the household level across Canada, with multiple household-level observations available within many FSAs. For each household, we defined a binary indicator of elevated radon risk, where radon concentration greater than 200 Bq/m$^3$ was assigned a value of 1 and 0 otherwise. We then aggregated these household-level indicators within each FSA to obtain an FSA-level fraction target representing the proportion of sampled homes with elevated radon risk.

2. Our predictive features include census-derived housing, demographic, and socioeconomic indicators, geological province and rock-type variables, surficial sedimentary types, uranium concentration, and heating degree day data. These datasets were spatially aligned, cleaned, and merged into a unified FSA-level modeling table, which was used to predict the FSA-level radon risk fraction.

### Modeling approach



### Results




### Conclusions



### Future plans



### Repo structure
