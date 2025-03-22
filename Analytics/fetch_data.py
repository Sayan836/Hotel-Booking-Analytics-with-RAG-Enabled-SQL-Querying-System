import pandas as pd
class FetchData():
  def __init__(self, dataset_path):
    self.dataset_path= dataset_path
  
  def read_data(self):
    df= pd.read_csv(self.dataset_path)
    return df
  
  def preprocess_data(self, df):
    selected_columns = [
    'hotel', 'is_canceled', 'lead_time', 'arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month',
    'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children', 'babies',
    'adr', 'country', 'market_segment', 'distribution_channel',
    'reserved_room_type', 'assigned_room_type', 'deposit_type', 'customer_type'
    ]
    df = df[selected_columns]

    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    df['arrival_date_month'] = df['arrival_date_month'].map(month_mapping)

    return df

  def load(self):
    df= self.read_data()
    df= self.preprocess_data(df)
    return df