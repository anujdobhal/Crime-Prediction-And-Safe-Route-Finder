import sys
import json
import joblib
import numpy as np
import pandas as pd

class CrimeRiskPredictor:
    def __init__(self, model_file=r'utility\trained_crime_model.pkl'):
        try:
            data = joblib.load(model_file)
            self.model = data['model']
        except Exception as e:
            print(f"Model loading error: {e}", file=sys.stderr)
            raise

    def predict_risk_score(self, data_array):
        try:
            # convert to DataFrame and rename keys
            df = pd.DataFrame(data_array)
            df.rename(columns={'lat': 'Latitude', 'lng': 'Longitude'}, inplace=True)

            # input only Latitude and Longitude columns
            X = df[['Latitude', 'Longitude']]

            if hasattr(self.model, "predict_proba"):
                proba = self.model.predict_proba(X)
                risk_scores = proba[:, 1] * 100  
                avg_risk = int(np.round(np.mean(risk_scores)))
                return avg_risk
            else:
                preds = self.model.predict(X)
                avg_risk = int(np.round(np.mean(preds) * 100))
                return avg_risk
        except Exception as e:
            print(f"Prediction error: {e}", file=sys.stderr)
            return 0

if __name__ == "__main__":
    try:
        input_data = json.loads(sys.stdin.read())
        coordinates = input_data.get("coordinates", [])

        predictor = CrimeRiskPredictor()
        risk_percentage = predictor.predict_risk_score(coordinates)

        print(risk_percentage)  # output for Node.js 
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print(0)

