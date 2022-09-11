# Capstone Project for MLOps Zoomcamp: Operationalizing Machine Learning for bank marketing campaigns


## Objective
Marketing to the clients (both prospects and current) has always been a crucial challenge in attaining success for financial institutions.
Accoring to the [Gartner](https://youtu.be/bXob4SMBguM?t=1824), marketing offers delivered in real time are *twise* more effisient then that made short time later, and *10X times* more succeful then made without considering current customer contxt 

This project utilizes Machine Learning Operations (MLOps) concepts to build a system for predicting response probality for targetet markteing campaging for a bank.</br>
Project includes model building with [Catboost](https://catboost.ai/, one of the most efficient alorythms for tabular data.</br>
After model training **online model scoring service** will be created  for the prediction of customers who will respond to the communication and will open a deposit in the bank. </br>
The main focus of the project is to make a process for **end-to-end model lifecylce** including experiment tracking, pipeline automation, monitoring and re-training. <br/>

## Dataset
Data source: https://archive.ics.uci.edu/ml/datasets/bank+marketing

The dataset was created by Angeliki Xifara (angxifara '@' gmail.com, Civil/Structural Engineer) and was processed by Athanasios Tsanas (tsanasthanasis '@' gmail.com, Oxford Centre for Industrial and Applied Mathematics, University of Oxford, UK).

### Data Set Information:

It is a dataset that describing Portugal bank marketing campaigns results. Conducted campaigns were based mostly on direct phone calls, offering bank client to place a term deposit. </br>
If after all marketing efforts client had agreed to place deposit - target variable marked 'yes', otherwise 'no'

### Attribute Information:

Input variables:
#### bank client data:
1 - age (numeric)
2 - job : type of job (categorical: 'admin.','blue-collar','entrepreneur','housemaid','management','retired','self-employed','services','student','technician','unemployed','unknown')
3 - marital : marital status (categorical: 'divorced','married','single','unknown'; note: 'divorced' means divorced or widowed)
4 - education (categorical: 'basic.4y','basic.6y','basic.9y','high.school','illiterate','professional.course','university.degree','unknown')
5 - default: has credit in default? (categorical: 'no','yes','unknown')
6 - housing: has housing loan? (categorical: 'no','yes','unknown')
7 - loan: has personal loan? (categorical: 'no','yes','unknown')
#### related with the last contact of the current campaign:
8 - contact: contact communication type (categorical: 'cellular','telephone')
9 - month: last contact month of year (categorical: 'jan', 'feb', 'mar', ..., 'nov', 'dec')
10 - day_of_week: last contact day of the week (categorical: 'mon','tue','wed','thu','fri')
11 - duration: last contact duration, in seconds (numeric). Important note: this attribute highly affects the output target (e.g., if duration=0 then y='no'). Yet, the duration is not known before a call is performed. Also, after the end of the call y is obviously known. Thus, this input should only be included for benchmark purposes and should be discarded if the intention is to have a realistic predictive model.
#### other attributes:
12 - campaign: number of contacts performed during this campaign and for this client (numeric, includes last contact)
13 - pdays: number of days that passed by after the client was last contacted from a previous campaign (numeric; 999 means client was not previously contacted)
14 - previous: number of contacts performed before this campaign and for this client (numeric)
15 - poutcome: outcome of the previous marketing campaign (categorical: 'failure','nonexistent','success')

### Relevant Papers:

S. Moro, P. Cortez and P. Rita. A Data-Driven Approach to Predict the Success of Bank Telemarketing. Decision Support Systems, Elsevier, 62:22-31, June 2014

S. Moro, R. Laureano and P. Cortez. Using Data Mining for Bank Direct Marketing: An Application of the CRISP-DM Methodology. In P. Novais et al. (Eds.), Proceedings of the European Simulation and Modelling Conference - ESM'2011, pp. 117-121, Guimaraes, Portugal, October, 2011. EUROSIS.





## Keep in touch
Artem Glazkov, slania.russia@gmail.com