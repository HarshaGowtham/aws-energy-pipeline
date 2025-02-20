import boto3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "EnergyData"
table = dynamodb.Table(TABLE_NAME)

# Fetch data from DynamoDB
def fetch_data():
    response = table.scan()
    items = response.get("Items", [])

    # Convert to DataFrame
    df = pd.DataFrame(items)
    
    # Convert numeric fields from string to float
    df["energy_generated_kwh"] = df["energy_generated_kwh"].astype(float)
    df["energy_consumed_kwh"] = df["energy_consumed_kwh"].astype(float)
    df["net_energy_kwh"] = df["net_energy_kwh"].astype(float)
    
    # Convert timestamp to datetime
    df["record_timestamp"] = pd.to_datetime(df["record_timestamp"])
    
    return df

# Plot Energy Generated vs. Energy Consumed
def plot_energy(df):
    plt.figure(figsize=(12, 6))
    
    df = df.sort_values("record_timestamp")

    sns.lineplot(data=df, x="record_timestamp", y="energy_generated_kwh", label="Generated", marker="o", linewidth=2, linestyle="-", color="blue")
    sns.lineplot(data=df, x="record_timestamp", y="energy_consumed_kwh", label="Consumed", marker="s", linewidth=2, linestyle="--", color="orange")

    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Energy (kWh)", fontsize=12)
    plt.title("Energy Generated vs. Energy Consumed Over Time", fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    # Save as PNG
    plt.savefig("energy_trends.png")

    plt.show()




# Plot Net Energy Over Time
def plot_net_energy(df):
    plt.figure(figsize=(12, 6))
    
    df = df.sort_values("record_timestamp")

    sns.barplot(data=df, x="record_timestamp", y="net_energy_kwh", palette="coolwarm")

    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Net Energy (kWh)", fontsize=12)
    plt.title("Net Energy Over Time", fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.7)

    # Save as PNG
    plt.savefig("net_energy_trends.png")

    plt.show()


# Plot Anomalies
def plot_anomalies(df):
    plt.figure(figsize=(12, 6))

    # Sort values by timestamp
    df = df.sort_values("record_timestamp")

    # Separate normal and anomaly data
    normal_data = df[df["anomaly"] == False]
    anomaly_data = df[df["anomaly"] == True]

    # Plot normal data in green
    plt.scatter(normal_data["record_timestamp"], normal_data["net_energy_kwh"], color="green", label="Normal", alpha=0.7)

    # Plot anomaly data in red
    plt.scatter(anomaly_data["record_timestamp"], anomaly_data["net_energy_kwh"], color="red", label="Anomaly", alpha=0.9, marker="X", s=100)

    # Improve readability
    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Net Energy (kWh)", fontsize=12)
    plt.title("Anomalies in Energy Data", fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    # Save the plot as a PNG file
    plt.savefig("anomalies_plot.png")

    plt.show()


# Run visualizations
if __name__ == "__main__":
    df = fetch_data()
    
    if df.empty:
        print("No data found in DynamoDB!")
    else:
        plot_energy(df)
        plot_net_energy(df)
        plot_anomalies(df)
