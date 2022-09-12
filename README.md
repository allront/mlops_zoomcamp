![bank marketing campaign using ML](https://raw.githubusercontent.com/allront/mlops_zoomcamp/main/images/Deposit.jpg)

# Capstone Project for MLOps Zoomcamp: Operationalizing Machine Learning for a bank marketing campaigns

## Objective
Marketing to the clients (both prospects and current) has always been a crucial challenge in attaining success for financial institutions.</br>
According to the [Gartner](https://youtu.be/bXob4SMBguM?t=1824), marketing offers delivered in real time are **twice more efficient** then that made short time later, and **10X times more successful** then that made without considering current customer context.</br> 

This project utilizes Machine Learning Operations (MLOps) methods to build a system for predicting bank client probability to respond to marketing campaign made by different communication channels.</br>
Project includes model building with [Catboost](https://catboost.ai/), one of the most efficient algorithms for tabular data.</br>
After model training **online model scoring service** will be created for the prediction of customers who will respond to the communication and will open a deposit in the bank. </br>
The main focus of the project is to make a end-to-end process for a** model lifecycle** including experiment tracking, pipeline automation, monitoring and re-training. <br/>

## MLOps architecture

<img src="https://raw.githubusercontent.com/allront/mlops_zoomcamp/main/images/Architecture.JPG">

MLops architecture for the project consists of three layers: </br>
* model development </br>
* model governance </br>
* model execution </br>

Technologies used for each layer are described bellow. </br>

### Development layer
Development layer is used for acquiring training data for a model and model creation.
EDA and Hyper parameter tuning are out of the scope of the project.

#### Yandex Cloud BLOB storage
Training data is placed into cloud storage, and accessed each time training runs.
Data that has been downloaded from cloud data should be compared to expected by asserting function. This test is placed into file `test_function.py`

#### Yandex Catboost
<img src=https://i0.wp.com/neptune.ai/wp-content/uploads/When-to-Choose-CatBoost-Over-XGBoost-or-LightGBM-Practical-Guide_13.png width=50% height=50%>
CatBoost uses ordered target encoding, which essentially allows to keep the feature/column in its original state, allowing to collaborate with ml engineers and software engineers more easily. 
Thus, there is no reason to worry about matching one-hot-encodings of several features, and interpret the features as to how they were intended. 
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
In meanwhile, sklearn is used for:
* splitting the data set for train/test
* calculating model performance the metrics such as accuracy, f1, roc_auc

Training process is wrapped into a [prefect]( https://www.prefect.io/) flow, placed into file `train.py`
After training finishes, model score code, including `model.pkl` is placed into the folder `.\prediction_service\`.

### Governance layer
Governance layer is used for tracking the experiments, run orchestrated workflows to provide reproducibility into model lifecycle.

#### MLFlow
<img src=https://raw.githubusercontent.com/allront/mlops_zoomcamp/main/images/MLFlow.jpg>

In this project MFLow is used to track training runs (in terms of the tool - experiments), track parameters (such as model metrics on test data and hyper paraments) and artifact (such as model pickle file). </br>

After starting, MLFlow web UI is located at `http://localhost:3000`

#### Prefect
<img src=https://raw.githubusercontent.com/allront/mlops_zoomcamp/main/images/Prefect.jpg>

Prefect is used as a tool for orchestrating execution of training code. 
With possibility of scheduling, it will allow re-training of the model on the regular basis and maintain model performance on high level when the customer behavior changes and trends, captured truing previous model's run will became out-of-date.

After starting, Prefect service UI can be accessed using `http://localhost:4200/`

### Execution layer

#### Model scoring online service
Model file and scoring script is placed into the folder `.\prediction_service\`.
When you run `docker-compose`, it builds image and runs several container.
[Flask](https://flask.palletsprojects.com/en/2.2.x/) is used as a web-service for model and [mongodb](https://www.mongodb.com/) as a database for storing model results as well as predicion vectors.

#### Model Monitoring serivce
<img src="https://raw.githubusercontent.com/allront/mlops_zoomcamp/main/images/DataDrift.jpg">

[Evidently.Ai](https://evidentlyai.com/) is used for tracking model performance after deployment. </br>
It tracks data drift from features, consumed by models and display information at the [graphana](https://grafana.com/) dashbords. </br>
Reference data for data drift monitoring is placed at `.\evidently_service\datasets\test.csv` </br>
Monitoring configuration is placed at `.\evidently_service\config.yaml` </br>

Evidenlty's reports at Graphana can be accessed by `http://localhost:3000`

## About Dataset
Data source: https://archive.ics.uci.edu/ml/datasets/bank+marketing
It is a dataset that describing Portugal bank marketing campaigns results. Conducted campaigns were based mostly on direct phone calls, offering bank client to place a term deposit. </br>
If after all marketing efforts client had agreed to place **deposit** - target variable marked 'yes', otherwise 'no'</br>

### Attribute Information:

#### bank client data:
**age** client's age </br>
**job** type of job </br>
**marital** marital status</br>
**education** clients education level </br>
**default** has credit in default?  </br>
**housing** has housing loan? </br>
**loan** has personal loan? </br>

#### related with the last contact of the current campaign:
**contact** contact communication type </br>
**month** last contact month of year</br>
**day_of_week** last contact day of the week </br>
**duration** last contact duration, in seconds. Important note: this attribute highly affects the output target (e.g., if duration=0 then y='no').</br> 
Yet, the duration is not known before a call is performed. Also, after the end of the call y is obviously known. </br>
Thus, this input should only be included for benchmark purposes and should be discarded if the intention is to have a realistic predictive model.</br>
#### other attributes:
**campaign** number of contacts performed during this campaign and for this client </br>
**pdays** number of days that passed by after the client was last contacted from a previous campaign</br>
**previous** number of contacts performed before this campaign and for this client </br>
**poutcome** outcome of the previous marketing campaign  </br>

### Relevant Papers:

* S. Moro, P. Cortez and P. Rita. A Data-Driven Approach to Predict the Success of Bank Telemarketing. Decision Support Systems, Elsevier, 62:22-31, June 2014 </br>

* S. Moro, R. Laureano and P. Cortez. Using Data Mining for Bank Direct Marketing: An Application of the CRISP-DM Methodology. In P. Novais et al. (Eds.), Proceedings of the European Simulation and Modelling Conference - ESM'2011, pp. 117-121, Guimaraes, Portugal, October, 2011 </br>

## Reproducing steps

* ```Git clone``` this repository to local pc or virtual pc on the cloud

* Run ```pipenv shell``` to install needed versions of the packages

* Run ```docker-compose up --build``` to start the prediction service as well as Graphana, Evidently and Prometeus

* Model scoring can be simulated by running ```model_scoring_simulation.py``` or ```test_request.py``` scripts

* Training the model could be started by ```train.py``` script. In case you want to use prefect, uncomment tasks and flow decorators

* Regular re-training can be started by ```schedule_deployment.py```. This script will schedule prefect flow that will place new model into MLFlow model registry

### Useful commands

start prefect: </br>
```prefect orion start --host 0.0.0.0```

start MLFlow server for tracking and model registry: </br>
```mlflow server --backend-store-uri sqlite:///mlruns.db  --default-artifact-root artifacts```

if graphana default authorization is not working: </br>
```grafana-cli admin reset-admin-password admin```

## Area of projcet improvement
List of the opportunities for improvements: <br/>

1) Add alerting, and automated re-train when the data drift/target drift/model accuracy degradation are detected.  </br>
2) Add IaC/cloud execution services. </br>
3) Add advanced capabilities to into model management part, such as model validation, ci/cd pipelines. </br>

## Special thanks go to
:thumbsup: Alexey Grigorev
:thumbsup: Emeli Dral
:thumbsup: Kevin Kho
:thumbsup: Sejal Vaidya
:thumbsup: Cristian Javier Martinez

## Keep in touch
Feedback is welcomed by :raising_hand_man: </br>
Artem Glazkov, slania.russia@gmail.com

