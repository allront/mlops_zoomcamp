![bank marketing campagin using ML](https://raw.githubusercontent.com/allront/mlops_zoomcamp/main/images/Deposit.jpg)


# Capstone Project for MLOps Zoomcamp: Operationalizing Machine Learning for bank marketing campaigns


## Objective
Marketing to the clients (both prospects and current) has always been a crucial challenge in attaining success for financial institutions.</br>
Accoring to the [Gartner](https://youtu.be/bXob4SMBguM?t=1824), marketing offers delivered in real time are `twise more effisient` then that made short time later, and `10X times more succeful` then made without considering current customer context.</br> 

This project utilizes Machine Learning Operations (MLOps) concepts to build a system for predicting response probality for targetet markteing campaging for a bank.</br>
Project includes model building with [Catboost](https://catboost.ai/), one of the most efficient alorythms for tabular data.</br>
After model training **online model scoring service** will be created  for the prediction of customers who will respond to the communication and will open a deposit in the bank. </br>
The main focus of the project is to make a process for **end-to-end model lifecylce** including experiment tracking, pipeline automation, monitoring and re-training. <br/>

## MLOps architecture

<img src="https://raw.githubusercontent.com/allront/mlops_zoomcamp/main/images/Architecture.JPG">

MLops architecture for the project consists of three layers: for machine learning model development, governance and execution.
The technologies used for each layer are described bellow

### Development layer
Development layer is used for aquiring the data for the model and model training.
EDA and Hyper parameter tuning is out of the scope of the project.

#### Yandex Cloud BLOB storage
Training data is placed into cloud storage, and accessed each time training is runned.
Downoladed data is compared to expeted result viaasserting function.
You may run this test via file `test_function.py`

#### Yandex Catboost
<img src=https://i0.wp.com/neptune.ai/wp-content/uploads/When-to-Choose-CatBoost-Over-XGBoost-or-LightGBM-Practical-Guide_13.png width=33% height=33%>
CatBoost uses ordered target encoding, which essentially allows to keep the feature/column in its original state, allowing to collaborate with ml engineers and software engineers more easily. 
Thus, ther is no reason to worry about matching one-hot-encodings of several features, and interpret the features as to how they were intended. 
Not only that, but this encoding allows for more important feature importance.

Here is the CatBoost space highlighted:
* No one-hot-encodings/sparse dataframe
* Keeps original format of dataframe, making collaboration easier as well
* Training is faster
* Categorical features are more important
* Model is more accurate
* It can work with features like ID’s, or categorical features with high unique counts

#### Scikit learn
Catboost provides broad integration with other packages, such as MLflow and scikit learn.
In times, sklearn is used for
* spliting the data set for train/test
* calculating model performance the metrics such as accuracy, f1, roc_auc

Trainig process is runned as a prefect flow, placed into file `train.py`
After training is complted model score code incuding `model.pkl` is placed into `.\prediction_service\`.

### Governance layer
Governance layer is used for tracking the expertiments, run orchestrated workflows to provide repoducibility into model lifecylce management.

#### MLFlow
<img src=https://raw.githubusercontent.com/allront/mlops_zoomcamp/main/images/MLFlow.jpg>

In this project MFLow is used to track training runs (in terms of the tool - experiments), track parameters (such as model metrics on test data and hyper paraments) and artifact (such as model pickle files and other model files). </br>
MLFlow web UI is located at `localhost:3000`


#### Prefect
<img src=https://raw.githubusercontent.com/allront/mlops_zoomcamp/main/images/Prefect.jpg>

Prefect is used as a tool for execution of training code. 
With possibility of scheduling it will allow re-training of the model on the regular basis and maintain model perfomance on high level when the customer behaviour chages and trends, captured turing previous model's run will became out-of-date.

### Exectuion layer

#### Model scoring online service
Model file and scoring script is placed into the folder `.\prediction_service\`.
When you run docker-compose file, it build image and runs container for the that image.
[Flask](https://flask.palletsprojects.com/en/2.2.x/) is used as a web-service for model and [mongodb](https://www.mongodb.com/) as a database for storing model results as well as predicion vectors.

#### Model Monitoring serivce
<img src="https://raw.githubusercontent.com/allront/mlops_zoomcamp/main/images/DataDrift.jpg">

[Evidently.Ai](https://evidentlyai.com/) is used for tracking model perfomance after deployment. It will track data drift from features, consumed by models and display information at the [graphana](https://grafana.com/) Dashbords

* Scoring simulation can be done using using</br>
`model_scoring_simulation.py`
* or run single request using </br>
`test_request.py`
* to access Evidenlty's reports Graphana is availible by
`localhost:3000`

## About Dataset
Data source: https://archive.ics.uci.edu/ml/datasets/bank+marketing
It is a dataset that describing Portugal bank marketing campaigns results. Conducted campaigns were based mostly on direct phone calls, offering bank client to place a term deposit. </br>
If after all marketing efforts client had agreed to place `deposit` - target variable marked 'yes', otherwise 'no'</br>

### Attribute Information:

Input variables:

#### bank client data:
`age` client's age (numeric)</br>
`job` type of job (categorical: 'admin.','blue-collar','entrepreneur','housemaid','management','retired','self-employed','services','student','technician','unemployed','unknown') </br>
`marital` marital status (categorical: 'divorced','married','single','unknown'; note: 'divorced' means divorced or widowed) </br>
`education` (categorical: 'basic.4y','basic.6y','basic.9y','high.school','illiterate','professional.course','university.degree','unknown') </br>
`default` has credit in default? (categorical: 'no','yes','unknown') </br>
`housing` has housing loan? (categorical: 'no','yes','unknown') </br>
`loan` has personal loan? (categorical: 'no','yes','unknown') </br>

#### related with the last contact of the current campaign:
`contact` contact communication type (categorical: 'cellular','telephone')</br>
`month` last contact month of year (categorical: 'jan', 'feb', 'mar', ..., 'nov', 'dec')</br>
`day_of_week` last contact day of the week (categorical: 'mon','tue','wed','thu','fri')</br>
`duration` last contact duration, in seconds (numeric). Important note: this attribute highly affects the output target (e.g., if duration=0 then y='no').</br> 
Yet, the duration is not known before a call is performed. Also, after the end of the call y is obviously known. </br>
Thus, this input should only be included for benchmark purposes and should be discarded if the intention is to have a realistic predictive model.</br>
#### other attributes:
`campaign` number of contacts performed during this campaign and for this client (numeric, includes last contact) </br>
`pdays` number of days that passed by after the client was last contacted from a previous campaign (numeric; 999 means client was not previously contacted) </br>
`previous` number of contacts performed before this campaign and for this client (numeric) </br>
`poutcome` outcome of the previous marketing campaign (categorical: 'failure','nonexistent','success') </br>

### Relevant Papers:

S. Moro, P. Cortez and P. Rita. A Data-Driven Approach to Predict the Success of Bank Telemarketing. Decision Support Systems, Elsevier, 62:22-31, June 2014 </br>
S. Moro, R. Laureano and P. Cortez. Using Data Mining for Bank Direct Marketing: An Application of the CRISP-DM Methodology. In P. Novais et al. (Eds.), Proceedings of the European Simulation and Modelling Conference - ESM'2011, pp. 117-121, Guimaraes, Portugal, October, 2011. EUROSIS. </br>


## Reproducing steps

* ```Git clone``` this repository to local pc or virtual pc on the cloud

* Run ```python -n pipenv shell``` to install use needed version of the packages

* Run ```docker-compose up --build``` to start the predicion service as well as Graphana, Evidently and Prometeus

* Scoring can be simulated by running ```model_scoring_simulation.py``` script

* Regular re-training can be runned by ```schedule_deployment.py```. It will start scheduled prefect flow that will place new model regulary into MLFlow model registry

### useful commands

start prefect: </br>
```prefect orion start --host 0.0.0.0```

start MLFlow server for tracking and model registry: </br>
```mlflow server --backend-store-uri sqlite:///mlruns.db  --default-artifact-root artifacts```

if graphana default authorization is not working: </br>
```grafana-cli admin reset-admin-password admin```


## Area of projcet improvement
List of the oppoptunities for improvements, for example: <br/>

1) Add alerting, and automated re-train when the data/target drift are detected.  </br>
2) Add IaC or cloud execution services </br>
3) Add advanced capabilites to into model management part, such as model validation and ci/cd pipelines. </br>

## Special thanks goes to:

## Keep in touch
Artem Glazkov, slania.russia@gmail.com