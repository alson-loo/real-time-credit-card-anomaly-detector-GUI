import os
import modules.scale_train as st
from datetime import datetime

def schedule_train(scalertype_config, shuffletype_config, tt_split_config, batch_config, epoch_config, time_config):
    while os.path.exists(r'.\data\stop.txt')==False:
        if datetime.now().strftime("%H:%M:%S") == time_config:
            print('\n ********schedule_train start********', datetime.now())
            st.scale_train_db(scalertype_config, shuffletype_config, tt_split_config, batch_config, epoch_config)
            print('training started')

    print('\n ********schedule_train stop********')
