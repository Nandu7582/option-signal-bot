import pandas as pd
import os

def save_signal(signal):
    path = "signals.csv"
    df = pd.DataFrame([signal])
    if os.path.exists(path):
        df.to_csv(path, mode='a', header=False, index=False)
    else:
        df.to_csv(path, index=False)
