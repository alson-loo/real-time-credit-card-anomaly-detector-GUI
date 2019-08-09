###Real-time credit card fraud anomaly detector with GUI

This is my final capstone project which implements a GUI for a role-based system using multi-layer perceptron to detect anomalies written in python. The supervisor decides on the model hyperparameters and the time for automatic retraining. While the analyst changes any misclassifications by the system if any customer calls in to clarify on the transactions being misclassified. The model learns from any misclassification and accuracy improves. When in detection mode, the supervisor can log out and switch user while the analyst can log in and do the neccessary misclassifications adjustments with detection still running in the background without blocking the UI. Any adjustments made to the database will be logged for accountability.

**System Architecture**

![alt text](https://github.com/alson-loo/real-time-credit-card-anomaly-detector-GUI/blob/master/images/architecture.png)



**Screen Design**


![alt text](https://github.com/alson-loo/real-time-credit-card-anomaly-detector-GUI/blob/master/images/screen_design.png)


**User Guide**

Please download the kaggle credit card fraud dataset and place the csv file in the data folder before use.
https://www.kaggle.com/mlg-ulb/creditcardfraud/version/3


![alt text](https://github.com/alson-loo/real-time-credit-card-anomaly-detector-GUI/blob/master/images/user_guide.png)

**Installation**

Please view the **requirements.txt** for the required libraries to use the software.

**Conclusions**

Regarding the capstone project, I felt that it can be further improved. Although accuracy is already high, it would be interesting to find out about the effectiveness of other methods and at the same time improve my own skills. For example, an ensemble of models can be used where their output would be probability distributions. To do that we have to use the functional api of Keras instead of the sequential api which the former allows more flexibility. LSTM can be employed to help forecast and alert the user several steps ahead before a possible fraud might happen and a multi-level perceptron model to classify if that step is a true fraud class, where each of the models would be given weights to create a final classification.  For the capstone project, the layouts of the screens certainly can be improved for more user friendliness. As for data storage, a temporary database should be created to store all incoming transactions and batch prediction done on them instead of predicting one at a time. The reason is because of the veracity of data in real life cases, the prediction one at a time would not be able to keep up with how fast the data is coming in. After prediction, the batch that was retrieved from the temporary database would be deleted and moved to the main database. 
