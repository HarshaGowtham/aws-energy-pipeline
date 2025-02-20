# AWS Energy Data Pipeline 🚀  

## 📌 Project Overview  
This project is an **end-to-end data pipeline** for processing **energy data** using **AWS services**. It simulates a real-world scenario where energy data is collected, processed, and stored in DynamoDB.  

## 🏗️ Architecture  
🔹 **S3 Bucket:** Stores raw energy data files  
🔹 **AWS Lambda (Processing):** Extracts and transforms data from S3  
🔹 **DynamoDB:** Stores processed energy data  
🔹 **AWS Lambda (Query API):** Allows querying data via API Gateway  
🔹 **API Gateway:** Exposes an endpoint for external queries  
🔹 **SNS:** Sends anomaly alerts via email  

## 🛠️ Technologies Used  
✅ AWS (S3, Lambda, DynamoDB, API Gateway, SNS)  
✅ Python (boto3, pandas, matplotlib)  
✅ GitHub Actions (CI/CD for AWS Lambda Deployment)  

## 📂 Folder Structure  
aws-energy-pipeline/ │── .github/workflows/ # GitHub Actions for CI/CD
│── process_energy_data.py # Lambda function (Processing)
│── query_energy_data.py # Lambda function (Query API)
│── visualize_energy_data.py # Data visualization script
│── generate_data.py # Generates sample data
│── requirements.txt # Python dependencies
│── README.md # Documentation
│── energy_trends.png # Graph: Energy Trends
│── anomalies_plot.png # Graph: Anomaly Detection
│── net_energy_trends.png # Graph: Net Energy



## 🚀 How to Run Locally  
1️⃣ **Clone the Repository**  
```sh
git clone https://github.com/HarshaGowtham/aws-energy-pipeline.git
cd aws-energy-pipeline


Set Up Python Environment

python -m venv venv
venv\Scripts\activate   # For Windows
pip install -r requirements.txt


Generate Sample Data & Upload to S3
python generate_data.py


How to Query Data via API

Send a GET request to API Gateway:

https://your-api-gateway-url/query_energy_data?site_id=12345

Example Response (JSON):

[
  {
    "site_id": "12345",
    "timestamp": "2025-02-19T21:46:30.822517",
    "energy_generated_kwh": 77.9,
    "energy_consumed_kwh": 332.77,
    "net_energy_kwh": -254.87,
    "anomaly": false
  }
]


📊 Data Visualization
Run the following command to generate energy data visualizations:

python visualize_energy_data.py

It produces graphs like:
📌 Energy Trends → energy_trends.png
📌 Net Energy Trends → net_energy_trends.png
📌 Anomaly Detection → anomalies_plot.png

🔔 Extra Credit: SNS Email Alerts
If an anomaly is detected (negative energy values), an AWS SNS alert is triggered.
The alert is sent via email (configured in AWS SNS).

✅ Submission Details
GitHub Repo: https://github.com/HarshaGowtham/aws-energy-pipeline
Video Link: https://www.loom.com/share/68e9c8f14b1d49e1892915c53329f7d3


---

### **✅ Step 3: Save the README File**  
📌 **Once pasted in Notepad, save the file:**  
1️⃣ **Click** → "File" > "Save"  
2️⃣ **Close Notepad**  

---

### **✅ Step 4: Push the README.md to GitHub**
Run these commands in **Command Prompt (cmd):**  
```cmd
git add README.md
git commit -m "Added full project documentation"
git push origin main



