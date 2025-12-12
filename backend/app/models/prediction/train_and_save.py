import pandas as pd
import numpy as np
import datetime
import os
import pickle
import json
import joblib

# Ensure we are in the right directory or handle paths
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.models.prediction.demand_prediction_engine import DataGenerator, FeatureEngineer, ProphetWrapper, XGBoostWrapper, LSTMWrapper

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

def save_model(model, filename):
    path = os.path.join(MODEL_DIR, filename)
    print(f"Saving {filename} to {path}...")
    if filename.endswith('.pkl'):
        with open(path, 'wb') as f:
            pickle.dump(model, f)
    elif filename.endswith('.json'):
        # XGBoost save
        model.save_model(path)
    elif filename.endswith('.keras'):
        # Keras save
        model.save(path)
    elif filename.endswith('.joblib'):
         joblib.dump(model, path)
    else:
        print(f"Unknown format for {filename}")

def train_and_save_all():
    print("--- Starting One-Time Model Training & Serialization ---")
    
    # 1. Generate Data (or load from DB if available, but for bootstrapping we use synthetic matching DB schema)
    print("Generating training data...")
    gen = DataGenerator(days=90)
    raw_df = gen.generate()
    
    # 2. Process
    fe = FeatureEngineer()
    df_model, df_full, _ = fe.process(raw_df)
    
    # 3. Train & Save Prophet
    print("Training Prophet...")
    pw = ProphetWrapper()
    pw.train(df_full)
    # Prophet serialization: pickle is standard for Prophet
    save_model(pw.model, "prophet_model.pkl")
    
    # 4. Train & Save XGBoost
    print("Training XGBoost...")
    xw = XGBoostWrapper()
    xw.train(df_model)
    # XGBoost supports json
    save_model(xw.model, "xgboost_model.json")
    
    # 5. Train & Save LSTM
    print("Training LSTM...")
    lw = LSTMWrapper(look_back=24)
    lw.train(df_model)
    # Save Keras model
    save_model(lw.model, "lstm_model.keras")
    # Save Scaler (needed for inference)
    save_model(lw.scaler, "lstm_scaler.pkl")
    
    print("\n--- All models saved successfully! ---")
    print(f"Location: {MODEL_DIR}")

if __name__ == "__main__":
    train_and_save_all()
