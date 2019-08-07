import os
import datetime
import sqlite3
import pandas as pd
import numpy as np
import warnings
import tensorflow as tf
import joblib
from keras.models import load_model
from keras import backend as K


def simulate_predict(model_config):

    print('--------simulate start--------')
    # remove verbose
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.logging.set_verbosity(tf.logging.ERROR)
    warnings.filterwarnings('ignore')

    # load scaler
    #dir_name = '.\models'
    model_filename = model_config
    scaler_filename = model_filename[:-9] + '.save'
    scaler = joblib.load(r'./models/' + scaler_filename)

    # connect to database to insert predicted
    con1 = sqlite3.Connection(r'.\data\creditcard.db')
    con1.execute("PRAGMA journal_mode=WAL")

    # load prepared simulation data
    df = pd.read_csv(r'.\data\data_simulate.csv', index_col='id')

    # scale transform incoming data from saved scaler
    for i in range(len(df)):
        start = datetime.datetime.now() # start timing total time needed for prediction
        check_incoming = df.iloc[[i]]
        check_incoming.insert(30, 'Amount_Norm', scaler.transform(check_incoming.loc[:,'Amount'].to_numpy().reshape(-1,1)))
        check_incoming_new = check_incoming.drop(['Amount', 'CheckBy', 'Class', 'Time'], axis=1)

        # start prediction
        tf.reset_default_graph()
        #config = tf.ConfigProto(device_count={'GPU': 0}) #if want to use cpu
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        with tf.Session(config=config) as sess:

            K.set_session(sess)
            classifier = load_model(r'./models/' + model_filename)
            y_pred = classifier.predict(check_incoming_new.to_numpy().flatten().reshape(-1, 29))
            print(y_pred)
            if y_pred > 0.5:
                print(i)
                print(datetime.datetime.now(), 'alert! anomaly detected', np.rint(y_pred))
                df.loc[i:i+1, 'Class'] = 1
                temp_df = df.iloc[[i]]
                temp_df.to_sql('transactions', con1, if_exists='append', index=False)
            else:
                print(i)
                df.loc[i:i+1, 'Class'] = 0
                temp_df = df.iloc[[i]]
                temp_df.to_sql('transactions', con1, if_exists='append', index=False)
                print('no prob')

        sess.close()

        end = datetime.datetime.now()
        print('time taken : ', (end - start))
        #time.sleep(2)

        if os.path.exists(r'.\data\stop.txt'):
            break

    # close database connection
    con1.close()
    print('--------simulate stop--------')
