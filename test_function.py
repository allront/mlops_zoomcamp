import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

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

def test_get_training_data(url):
    '''
    Makes the unit test for the function "make_label_encoding"
    returns None if the expected result is equivalent to the actual result,
    returns difference otherwise
    '''
    Xactual, Yactual=get_training_data(url)

    df = pd.read_csv('integration_tests/bank.csv')
    
    df['target'] = np.where(df['deposit'] == "yes", 1, 0)
    df.drop(['duration','deposit'], inplace=True, axis=1)

    X_expected = df.drop("target", axis=1)
    y_expected = df["target"]

    assertionTrain = assert_frame_equal(Xactual, X_expected)
    
    assert assertionTrain is None
    
    assertionTest = assert_frame_equal(pd.DataFrame(Yactual), pd.DataFrame(y_expected))
    
    assert assertionTest is None

url = "https://storage.yandexcloud.net/mlopsdatatalksbucket/bank.csv"
test_get_training_data(url)