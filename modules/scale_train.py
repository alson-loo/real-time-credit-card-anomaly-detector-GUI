import sqlite3
import pandas as pd
import joblib
import os
import tensorflow as tf
from datetime import datetime
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras import backend as K


def scale_train_db(scalertype_config, shuffletype_config, tt_split_config, batch_config, epoch_config):
    print('scaler : {}, shuffle : {}, tt_split : {}, batch : {}, epoch : {}'.format(scalertype_config, shuffletype_config, tt_split_config, batch_config, epoch_config))

    # Extract data from database into dataframe
    con = sqlite3.Connection(r'.\data\creditcard.db')
    con.execute("PRAGMA journal_mode=WAL")
    df = pd.read_sql_query("SELECT * FROM transactions", con)

    # prepare for naming convention
    dir_name = r'.\models'
    dt_string = datetime.now().strftime('%Y%m%d_%H%M')

    # fit / transform data from database with selected scaler and save
    if scalertype_config=="Scaler:StandardScaler":
        sscaler = StandardScaler().fit(df['Amount'].values.reshape(-1, 1))
        scaler_filename = dt_string + ".save"
        file = os.path.join(dir_name, scaler_filename)
        joblib.dump(sscaler, file)
        df['Amount_norm'] = sscaler.transform(df['Amount'].values.reshape(-1, 1))
        df.drop(['Amount', 'Time', 'CheckBy', 'id'], inplace=True, axis=1)
    else:
        mmscaler = MinMaxScaler().fit(df['Amount'].values.reshape(-1, 1))
        scaler_filename = dt_string + ".save"
        file = os.path.join(dir_name, scaler_filename)
        joblib.dump(mmscaler, file)
        df['Amount_norm'] = mmscaler.transform(df['Amount'].values.reshape(-1, 1))
        df.drop(['Amount', 'Time', 'CheckBy', 'id'], inplace=True, axis=1)

    # Train/test split
    X = df.iloc[:, df.columns != 'Class']
    y = df.iloc[:, df.columns == 'Class']
    if shuffletype_config=="Shuffle:Yes": shuffle=True
    else: shuffle=False

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=tt_split_config, shuffle=shuffle)

    # config to overcome the errors arising from using threads to run tensorflow
    tf.reset_default_graph()
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
        K.set_session(sess)

        # Initialise Neural Network
        classifier = Sequential()
        classifier.add(Dense(units=15, kernel_initializer='uniform', activation='relu', input_dim=29))
        classifier.add(Dense(units=15, kernel_initializer='uniform', activation='relu'))
        classifier.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))
        classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # fit the NN to the Training set
        classifier.fit(X_train, y_train, batch_size=batch_config, epochs=epoch_config)

        # evaluate mode
        _, accuracy = classifier.evaluate(X_test, y_test)
        print(accuracy)

        # rename model and scaler with date and accuracy for retrieval later
        ac_str = str(int(accuracy * 100000))
        model_name = dt_string + '_' + ac_str + ".h5"
        file = os.path.join(dir_name, model_name)

        # save classifier model for later predictions

        classifier.save(file)
        print(classifier.summary())
        sess.close()

    print('Done training and saving all models')
