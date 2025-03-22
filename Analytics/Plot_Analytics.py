import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import base64

class PlotAnalytics():
  def __init__(self, df):
    self.df = df
  
  def get_plot_image(self):
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    encoded_img = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    return encoded_img

  def plot_revenue_trends(self):
    # Select relevant columns
    selected_columns = [
        'hotel', 'is_canceled', 'arrival_date_year', 'arrival_date_month',
        'stays_in_week_nights', 'stays_in_weekend_nights', 'adr'
    ]
    temp_df = self.df[selected_columns]

    # Remove canceled bookings
    temp_df = temp_df[temp_df['is_canceled'] == 0]

    # Handle missing values (replace ADR=0 with average per hotel)
    temp_df= temp_df[temp_df['adr']!=0]

    # Calculate total revenue per booking
    temp_df['total_revenue'] = temp_df['adr'] * (temp_df['stays_in_week_nights'] + temp_df['stays_in_weekend_nights'])

    # Group by Year and Month to get revenue trends
    revenue_trends = temp_df.groupby(['arrival_date_year', 'arrival_date_month'])['total_revenue'].sum().reset_index()


    # Sort data for proper visualization
    revenue_trends.sort_values(by=['arrival_date_year', 'arrival_date_month'], inplace=True)

    # Plot revenue trends
    plt.figure(figsize=(12,6))
    sns.lineplot(data=revenue_trends, x='arrival_date_month', y='total_revenue', hue='arrival_date_year', marker="o")
    plt.title("Hotel Revenue Trends Over Time")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue (€)")
    plt.legend(title="Year")
    plt.grid(True)
    encoded_img= self.get_plot_image()
    return encoded_img

  def plot_cancellation_rate(self):
    # Select relevant columns
    selected_columns = ['hotel', 'is_canceled', 'arrival_date_year', 'arrival_date_month']
    temp_df = self.df[selected_columns]

    # Group by Year and Month to count total bookings and cancellations
    cancel_trends = temp_df.groupby(['arrival_date_year', 'arrival_date_month'])['is_canceled'].agg(['sum', 'count']).reset_index()

    # Calculate cancellation rate (%)
    cancel_trends['cancellation_rate'] = (cancel_trends['sum'] / cancel_trends['count']) * 100

    # Sort data for proper visualization
    cancel_trends.sort_values(by=['arrival_date_year', 'arrival_date_month'], inplace=True)
    # Plot cancellation rate trends
    plt.figure(figsize=(12,6))
    sns.lineplot(data=cancel_trends, x='arrival_date_month', y='cancellation_rate', hue='arrival_date_year', marker="o")
    plt.title("Hotel Cancellation Rate Over Time")
    plt.xlabel("Month")
    plt.ylabel("Cancellation Rate (%)")
    plt.legend(title="Year")
    plt.grid(True)
    encoded_img= self.get_plot_image()
    return encoded_img
  
  def plot_geographical_distribution(self):
    # Select relevant columns
    selected_columns = ['hotel', 'country']
    temp_df = self.df[selected_columns]

    # Drop missing values in country column
    temp_df = temp_df.dropna(subset=['country'])

    # Count bookings per country
    country_counts = temp_df['country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Bookings']

    # Filter top 20 countries for readability
    top_countries = country_counts.head(20)

    # Plot booking distribution
    plt.figure(figsize=(12,6))
    sns.barplot(data=top_countries, x='Country', y='Bookings', palette='viridis')
    plt.title("Top 20 Countries by Number of Hotel Bookings")
    plt.xlabel("Country")
    plt.ylabel("Number of Bookings")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    encoded_img= self.get_plot_image()
    return encoded_img
  
  def plot_lead_time_distribution(self):
    # Select relevant column
    selected_columns = ['lead_time']
    temp_df = self.df[selected_columns]

    # Plot lead time distribution
    plt.figure(figsize=(12,6))
    sns.histplot(temp_df['lead_time'], bins=50, kde=True, color='royalblue')
    plt.title("Booking Lead Time Distribution")
    plt.xlabel("Lead Time (Days)")
    plt.ylabel("Number of Bookings")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    encoded_img= self.get_plot_image()
    return encoded_img
  
  def plot_market_segment_pie(self):
    # Select relevant column
    selected_columns = ['market_segment']
    temp_df = self.df[selected_columns]

    # Count bookings per market segment
    segment_counts = temp_df['market_segment'].value_counts()

    # Define colors for better visualization
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6', '#ff6666']

    # Plot market segment distribution as a pie chart
    plt.figure(figsize=(10,6))
    plt.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title("Market Segment Preferences in Hotel Bookings")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    encoded_img= self.get_plot_image()
    return encoded_img
  
  def plot_booking_patterns_duration(self):
    # Select relevant columns
    selected_columns = ['stays_in_weekend_nights', 'stays_in_week_nights']
    temp_df = self.df[selected_columns]

    # Compute total stay duration
    temp_df['total_stay'] = temp_df['stays_in_weekend_nights'] + temp_df['stays_in_week_nights']

    # Plot booking duration distribution
    plt.figure(figsize=(12,6))
    sns.histplot(temp_df['total_stay'], bins=30, kde=True, color='purple')
    plt.title("Hotel Booking Duration Trends")
    plt.xlabel("Total Stay Duration (Nights)")
    plt.ylabel("Number of Bookings")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    encoded_img= self.get_plot_image()
    return encoded_img
  
  def analyze_data(self):
    plots={
        'revenue_trends': self.plot_revenue_trends(),
        'cancellation_rate': self.plot_cancellation_rate(),
        'geographical_distribution': self.plot_geographical_distribution(),
        'lead_time_distribution': self.plot_lead_time_distribution(),
        'market_segment_pie': self.plot_market_segment_pie(),
        'booking_patterns_duration': self.plot_booking_patterns_duration()
    }
    return plots
