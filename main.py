import os
import glob
import time
import modules.scale_train as st
import modules.simulate_incoming_predict as sim
import modules.schedule_train as sch
from threading import Thread
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, ObjectProperty
from kivy.uix.recycleview.views import _cached_views, _view_base_cache
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivy.config import Config
import sqlite3


# global variables
scalertype_config = "Scaler:StandardScaler"
shuffletype_config = "Shuffle:Yes"
tt_split_config = 0.8
batch_config = 100
epoch_config = 10
model_config = ""
time_config = "00:00:00"


class ConfirmPopup(Popup):
    pass


class SplashScreen(Screen):
    pass


class WelcomeScreen1(Screen):
    pass


class WelcomeScreen2(Screen):
    pass


class LoginPageScreen(Screen):
    def verify_credentials(self):
        if self.ids["user"].text == "supervisor" and self.ids["passw"].text == "password":
            self.manager.current = "modetype"
        elif self.ids["user"].text == "analyst" and self.ids["passw"].text == "password":
            self.manager.current = "dataamend"
        else:
            self.ids["user"].text = ""
            self.ids["passw"].text = ""

    def check_new(self):
        if glob.glob(r'./models/*.h5')==[]:
            return True
        else: return False


class ModeTypeScreen(Screen):
    def confirm_popup(self):
        ConfirmPopup().open()


class ModelSettingsScreen(Screen):
    btn_checkvaluesrun = ObjectProperty(None)

    def check_values_and_run(self):
        global model_config, time_config, scalertype_config, shuffletype_config, tt_split_config, batch_config, epoch_config
        if self.ids["spn_scalertype"].text == "Scaler:StandardScaler" or self.ids["spn_scalertype"].text == "Scaler:MinMaxScaler":
            scalertype_config = self.ids["spn_scalertype"].text
        if self.ids["spn_shuffletype"].text == "Shuffle:Yes" or self.ids["spn_shuffletype"].text == "Shuffle:No":
            shuffletype_config = self.ids["spn_shuffletype"].text
        if float(self.ids["tt_split"].text) > 0 and float(self.ids["tt_split"].text) <= 1:
            tt_split_config = float(self.ids["tt_split"].text)
        if int(self.ids["batch"].text) >= 1:
            batch_config = int(self.ids["batch"].text)
        if int(self.ids["epoch"].text) >= 1:
            epoch_config = int(self.ids["epoch"].text)

        print(model_config, time_config, scalertype_config, shuffletype_config, tt_split_config, batch_config, epoch_config)

        # Run scaling and train evaluate model
        st.scale_train_db(scalertype_config, shuffletype_config, tt_split_config, batch_config, epoch_config)


class TimeModelSelectScreen(Screen):
    def get_h5(self):
        files = [file for file in os.listdir(r'.\models') if (file.endswith('.h5'))]
        return files

    def check_time_selection(self):
        global time_config
        # check time selection
        hr, mm, ss = self.ids['settime'].text.split(':')
        if (hr.isdigit() and int(hr) <= 23 and int(hr) >= 0 and len(hr)==2) \
                and (mm.isdigit() and int(mm) <= 59 and int(mm) >= 0 and len(mm)==2) \
                and (ss.isdigit() and int(ss) <= 59 and int(ss) >= 0 and len(ss)==2):
            time_config = str(self.ids['settime'].text)
        else: time_config = "00:00:00"
        print(time_config)

    def check_model(self):
        global model_config
        model_config = str(self.ids['spn_selectmodel'].text)

    def run_thread(self):
        global model_config, time_config, scalertype_config, shuffletype_config, tt_split_config, batch_config,\
            epoch_config

        print(model_config, time_config)

        # run threads
        t1 = Thread(target=sim.simulate_predict, args=(model_config, ))
        t2 = Thread(target=sch.schedule_train, args=(scalertype_config, shuffletype_config, tt_split_config,
                                                     batch_config, epoch_config, time_config))
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()


    def stop_thread(self):
        # send close signal to scripts in order to close
        f = open(r".\data\stop.txt", "w+")
        f.close()
        time.sleep(4)
        os.remove(r".\data\stop.txt")


class DataAmendScreen(Screen):
    rows = ListProperty([("id", "Time", "Amount", "Class", "Checkby")])

    def get_zeros(self):
        con = sqlite3.connect(r'./data/creditcard.db')
        cur = con.cursor()
        cur.execute("SELECT id, Time, Amount, Class, Checkby From transactions WHERE Class = 0 AND CheckBy IN ('Analyst','machine')")
        self.rows = cur.fetchall()
        print(self.rows)
        con.close()

    def get_ones(self):
        con = sqlite3.connect(r'./data/creditcard.db')
        cur = con.cursor()
        cur.execute("SELECT id, Time, Amount, Class, Checkby From transactions WHERE Class = 1 AND CheckBy IN ('Analyst','machine')")
        self.rows = cur.fetchall()
        print(self.rows)
        con.close()

    def amend(self):
        input_amend = int(self.ids['ti_id_amend'].text)
        amend_bind = (input_amend, )
        con = sqlite3.connect(r'./data/creditcard.db')
        cur = con.cursor()
        cur.execute("PRAGMA journal_mode=WAL")
        cur.execute("SELECT id FROM transactions ORDER BY ID DESC LIMIT 1")
        lastrow = cur.fetchone()[0]
        cur.execute("SELECT Class FROM transactions WHERE id = ?", amend_bind)
        classtype = cur.fetchone()[0]
        if input_amend <= lastrow and input_amend >= 0 and classtype == 0:
            cur.execute("UPDATE transactions SET Class = 1, Checkby = 'Analyst' WHERE id = ?", amend_bind)
            con.commit()
        elif input_amend <= lastrow and input_amend >= 0 and classtype == 1:
            cur.execute("UPDATE transactions SET Class = 0, Checkby = 'Analyst' WHERE id = ?", amend_bind)
            con.commit()
        else: pass
        con.close()


class WindowManager(ScreenManager):
    splash = ObjectProperty(None)
    welcome1 = ObjectProperty(None)
    welcome2 = ObjectProperty(None)
    loginpage = ObjectProperty(None)
    modetype = ObjectProperty(None)
    modelsettings = ObjectProperty(None)
    timemodelselect = ObjectProperty(None)
    dataamend = ObjectProperty(None)


kv = Builder.load_file('main.kv')


class KivyGUI(App):
    def build(self):
        App.icon = r'.\data\images\icon_green.png'
        App.title = 'Fraud detector'
        Config.set('input', 'mouse', 'mouse,disable_multitouch')
        return kv


if __name__ == '__main__':
    KivyGUI().run()