import numpy as np
import pandas as pd
import sys
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


monthlydatalabelled = sys.argv[1]
monthlydataunlabelled = sys.argv[2]

def main():
	labelled = pd.read_csv(monthlydatalabelled)
	unlabelled = pd.read_csv(monthlydataunlabelled)
	X = labelled.drop('city',1).values
	y = labelled['city'].values
	X_train, X_test, y_train, y_test = train_test_split(X, y)

	svc_model = make_pipeline(
	        StandardScaler(),
	        SVC(kernel='linear', C=2.0)
	    )
	svc_model.fit(X_train, y_train)
	print('score:', svc_model.score(X_test, y_test))

	# df = pd.DataFrame({'truth': y_test, 'prediction': svc_model.predict(X_test)})
	# print(df[df['truth'] != df['prediction']])

	inputsForPrediction = unlabelled.drop('city', 1).values
	citiesPredicted = svc_model.predict(inputsForPrediction)
	pd.Series(citiesPredicted).to_csv(sys.argv[3], index=False)
    


if __name__ == '__main__':
    main()
