import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

class CrimeModelTrainer:
    def __init__(self):
        self.model = RandomForestClassifier()

    def fit(self, crime_data_array):
        crime_df = pd.DataFrame(crime_data_array)
        crime_df = crime_df[['Latitude', 'Longitude']]  # keep only coords
        crime_df['is_crime'] = 1  # label all known entries as crime

        # Generate non-crime data near the area
        non_crime_df = self.generate_negative_samples(crime_df, count=len(crime_df))
        full_df = pd.concat([crime_df, non_crime_df], ignore_index=True)

        X = full_df[['Latitude', 'Longitude']]
        y = full_df['is_crime']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        print(f"Model trained. Accuracy: {score * 100:.2f}%")
        return score

    def generate_negative_samples(self, df, count=100):
        lat_min, lat_max = df['Latitude'].min(), df['Latitude'].max()
        lng_min, lng_max = df['Longitude'].min(), df['Longitude'].max()

        np.random.seed(42)
        lats = np.random.uniform(lat_min - 0.01, lat_max + 0.01, count)
        lngs = np.random.uniform(lng_min - 0.01, lng_max + 0.01, count)

        return pd.DataFrame({
            'Latitude': lats,
            'Longitude': lngs,
            'is_crime': 0  # these are non-crime
        })

    def save_model(self, filename='crime_model.pkl'):
        joblib.dump({'model': self.model}, filename)
        #print(f"Model saved to {filename}")

    def load_model(self, filename='crime_model.pkl'):
        data = joblib.load(filename)
        self.model = data['model']


if __name__ == "__main__":
    # load crime data with Latitude and Longitude only
    df = pd.read_csv(r'utility\dummy_data.csv')
    data_array = df.to_dict(orient='records')

    # Train the model
    trainer = CrimeModelTrainer()
    trainer.fit(data_array)
    trainer.save_model(r'utility\trained_crime_model.pkl')

