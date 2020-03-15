# Data-Science
Course Projects During my Data Science studies

1.Data Exploration
1.1. Loading Data
Data was loaded from “GEO_DB_PS-20200113.xlsx", tab name="Cons for ANN". 

The size of the original data set is 91 rows and 29 columns.

1.2. Data Cleaning

A new data set was created by using only input (features) and output (targets) columns:
features=['Top_Depth','Easting','Northing','Class','e0','gd0','Gs','w0','OC']
targets=['Cce','Cre','Cae','OCR','CV']

The size of the new data set is 91 rows and 14 columns.

The following rows were deleted for consistency in data (this step can be revised, these values looked outlier to me based on the histograms):
Three rows with Soil Class equal to ‘other
Two rows with Gs = 8.41 and Gs= 0.27
Four rows with OC=NaN
One row with OCR= 38.37

The size of the new data set is 81 rows and 14 columns.


1.3.  Plotting Data
Easting-Northing plot show the location of the samples
Histograms shows the distribution of each feature
Pair-plot shows the relation between each pair of columns

2.Data Preparation
Using Standard scaler, all the features were scaled to improve the modelling. 
The data set was split to  80% full-training set and 20% test set. The full-training set was split to 80%  training set and 20% validation set. The number of the data set is as follows:

Geo_DB Size: (81, 14) 

X Train Size: (51, 9) 
X Validation Size: (13, 9) 
X Test Size (17, 9) 
 
y Train size: (51, 5) 
y Validation Size: (13, 5) 
y Test Size: (17, 5)
3.Regression Models (First file)
Four different regression models were used and compared. 
Support Vector Regressor
Decision Tree Regressor
K-Neighbors Regressor
Random Forest Regressor
 
For each model and each output parameter (targets=['Cce','Cre','Cae','OCR','CV']):
The model was trained using the training dataset
The validation data was used for predicting y_valid
The r-squared score of the actual y_valid and predicted_y_valid was calculated
The actual and predicted values were plotted

Also: 
Training dataset was used for training and cross validation of the model 
The r-squared score was calculated for five sets of cross validation sets
Conclusion: the wide range of the calculated R2_score for the cross validation shows the unreliability of the model. The main reason can be the small dataset. 


3.Neural Networks Models (Second file)
The main two steps are the same as the previous regression model. 
A general model with some default hyperparameters (n_hidden=1, n_neurons=30, learning_rate=3e-3) with 5 output was built. 

The model trained using training data set and MSE loss for the training and validation dataset was minimized during the run.

To fine tune the model,  random search cross validation was used and the best parameters were: {'learning_rate': 0.00228248110776524, 'n_hidden': 4, 'n_neurons': 45}

The r-squared score of the actual y_valid and predicted_y_valid was calculated and plotted. 

Conclusion: low values of calculated R2_score shows the unreliability of the model. The main reason can be the small dataset. 


