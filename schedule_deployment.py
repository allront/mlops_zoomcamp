from prefect import flow
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner

import pickle
import random

import numpy as np
import mlflow
import pandas as pd
from prefect import flow, task
from mlflow.tracking import MlflowClient
from sklearn.metrics import f1_score, recall_score, accuracy_score, precision_score,roc_auc_score
from catboost import CatBoostClassifier
from prefect.task_runners import SequentialTaskRunner
from sklearn.model_selection import train_test_split


@task
def get_training_data(url):
    '''
    Downloading data from cloud data storage
    Drop 'duration' because of high correlation with target, in order to build more insightful algorithm
    Encoding target column with 1 for event, i.e. response, and 0 for non-event
    '''
    df=pd.read_csv(url, header=0, sep=',')
    df['target'] = np.where(df['deposit'] == "yes", 1, 0)
    df.drop(['duration','deposit'], inplace=True, axis=1)

    X = df.drop("target", axis=1)
    y = df["target"]

    print("training dataset is ready")
    
    return X,y
    
@task
def train_model(X_train, y_train, X_val, y_val, random_state, cat_features):
    '''
    Using gradient boosting classifier by catboost for training ML model.
    Providing list of categorical variables
    '''
    
    iterations = 200
    learning_rate = 0.1
    l2_leaf_reg = 3
    bagging_temperature = 1
    random_strength = 1
    one_hot_max_size = 2
    leaf_estimation_method = 'Newton'
    
    model = CatBoostClassifier(
        random_seed=random_state,
        iterations=iterations,
        learning_rate=learning_rate,
        l2_leaf_reg=l2_leaf_reg,
        bagging_temperature=bagging_temperature,
        random_strength=random_strength,
        one_hot_max_size=one_hot_max_size,
        leaf_estimation_method=leaf_estimation_method
    )
    model.fit(
        X_train, y_train,
        cat_features=cat_features,
        verbose=False,
        eval_set=(X_val, y_val),
        plot=False
    )
    
    mlflow.log_params({
        "iterations": iterations, 
        "learning_rate": learning_rate,
        "l2_leaf_reg": l2_leaf_reg,
        "bagging_temperature": bagging_temperature,
        "random_strength": random_strength,
        "one_hot_max_size": one_hot_max_size,
        "leaf_estimation_method": leaf_estimation_method
    })
    
    print("training is complete")
    
    return model

@task
def calculate_metrics(model, X_test, test_target):
    '''
    Calculate accuracy, precision, recall, f1 and ROC AuC score metrics for a test data
    '''
    y_pred_test = model.predict(X_test)
    accuracy = accuracy_score(test_target, y_pred_test)
    precision = precision_score(test_target, y_pred_test)
    recall = recall_score(test_target, y_pred_test)
    f1 = f1_score(test_target, y_pred_test)
    roc_auc=roc_auc_score(test_target, y_pred_test)

    metrics_dict = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc":roc_auc,
    }
    
    print ("metrics calculation finished")
    
    return metrics_dict

@task
def save_model_file (model):
    '''
    Saves the new version of a model to the prediction_service/model.pkl
    '''
    with open('prediction_service/model.pkl', 'wb') as f_out:
        pickle.dump(model, f_out)

@task
def save_test_dataset(X_test):
    '''
    Rewrites test dataset for monitoring service in ./evidently_service/datasets/
    '''
    X_test.to_csv('evidently_service/datasets/test.csv', index_label='request_id')
    
    print("dataset is saved")



MLFLOW_TRACKING_URI = "sqlite:///mlruns.db"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("responce-prediction-experiment")


@flow(task_runner=SequentialTaskRunner())
def run():
    with mlflow.start_run() as run:

    with mlflow.start_run() as run:

        
        client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
        run_id = run.info.run_id
        model_uri = f"runs:/{run_id}/model"
        model_name = "responce-prediction-model"
        mlflow.set_tags({"developer": "Artem Glazkov", "project": "DataTalksClub Zoomcamp", "business area": "responce prediction"})
        
        url = "https://storage.yandexcloud.net/mlopsdatatalksbucket/bank.csv"

        X,y = get_training_data(url)
        
        cat_features = ['job','marital','education','default','housing','loan','contact','month','poutcome']

        random_state = random.randint(1, 100)

        mlflow.log_param("random state", random_state)
        
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.3, random_state=random_state
        )

        model = train_model(X_train, y_train, X_val, y_val, random_state, cat_features)        
        metrics_dict = calculate_metrics(model, X_val, y_val)
        
        try: 
            mlflow.log_metrics(metrics_dict)
        except: 
            print('there is an issue with logging metrics with mlflow + prefect')

        save_model_file(model)
        mlflow.sklearn.log_model(model, artifact_path="models")
        mlflow.register_model(model_uri=model_uri, name=model_name, tags={"developer": "Artem Glazkov", "project": "DataTalksClub Zoomcamp", "business area": "responce prediction"})

        client.transition_model_version_stage(
            name=model_name,
            version=1,
            stage="Production",
            archive_existing_versions=False,
        )
        save_test_dataset(X_val)
        


if __name__ == '__main__':

    Deployment(
        flow=run,
        name="responce-prediction-model",
        schedule=CronSchedule(cron="15 3 1 * *"), # At 03:15 on day-of-month 1 
        flow_runner=SubprocessFlowRunner(),
        tags=["final_project"]
    )
print("Deployment has been created")

