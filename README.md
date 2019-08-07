**<u>Real-time credit card fraud anomaly detector with GUI</u>**

This is my final capstone project which implements a GUI for a role-based system using multi-layer perceptron to detect anomalies written in python. The supervisor decides on the model hyperparameters and the time for automatic retraining. While the analyst changes any misclassifications by the system if any customer calls in to clarify on the transactions being misclassified. The model learns from any misclassification and accuracy improves. When in detection mode, the supervisor can log out and switch user while the analyst can log in and do the neccessary misclassifications adjustments with detection still running in the background without blocking the UI. Any adjustments made to the database will be logged for accountability.

**System Architecture**

![alt text](https://github.com/alson-loo/real-time-credit-card-anomaly-detector-GUI/blob/master/architecture.png)



**Screen Design**


![alt text](https://github.com/alson-loo/real-time-credit-card-anomaly-detector-GUI/blob/master/screen_design.png)


**User Guide**

Please download the kaggle credit card fraud dataset and place the csv file in the data folder before use.
https://www.kaggle.com/mlg-ulb/creditcardfraud/version/3


![alt text](https://github.com/alson-loo/real-time-credit-card-anomaly-detector-GUI/blob/master/user_guide.png)

**Installation**

Please view the **requirements.txt** for the required libraries to use the software.
