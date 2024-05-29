#  Anomaly detection in HPC systems

## Dataset
------------------------------
The data was collected from a monitored supercomputer hosted at CINECA and called "Marconi100"; the data was collected with a tool called Examon.
The dataset is composed of several folders, a folder for each selected node (there are not all the hundreds of nodes present on Marconi100, but some nodes with periods that also contained failures).
The information monitored on Marconi100's nodes is varied, ranging from the load of the different cores, to the temperature of the room where the nodes are located, the speed of the fans, details on memory accesses in writing / reading, etc
The sampling rate of the data at the source varies between 5 and 10 seconds.
However, in the data set the data are aggregated in 15-minutes intervals; in particular, the mean value ("avg: <metric_name>") and variance ("var: <metric_name>") are computed over each 15-minute interval.


## Task
-----------------------------------------
I performed an Anomaly detection using the three approaches semi supervised, unsupervised and self -supervised learning


## Models
-------------------------------------
I have used here models semi-supervised,unsupervised & self supervised algorithms. In order to make the comparision between the types of the model.
1. Autoencoders
2. Isolation Forest
3. Local Outlier Factor
4. One class SVM
5. Minimum Covariance Determinant
6. self supervised TABNET

## Supervised ,Unsupervised , Semi-supervised , Self-supervised

![Alt text](<images/Screenshot 2024-01-25 at 01.28.55.png>)

![Alt text](<images/Screenshot 2024-01-25 at 01.29.11.png>)

![Alt text](<images/Screenshot 2024-01-25 at 01.35.03.png>)

## Project WorkFlow
--------------------------------------------
1. Dataset Prepratation
2. Data Analysis
3. Split the data into training(Normal data)  and testing 
4. MinMax Scaling
5. Semi supervised Learning- Autoencoder
6. Reconstruction error check
7. chosing Threshold based on F1 score
8. Implementation of Unsupervised Algorithms
   * Isolation Forest
   * Local Outlier Factor
   * One class SVM
   * Minimum Covariance Determinant
9. self supervised using TABNET

## Results
![17](https://user-images.githubusercontent.com/72126242/180228565-41f7c7b8-f593-49d4-ad62-bae5c11cc62f.png)


## Built With
---------------------------------
Python 3.7

## Author
-------------------------------
[Jyoti Yadav](https://www.linkedin.com/in/jyoti-yadav-64916b160/)




