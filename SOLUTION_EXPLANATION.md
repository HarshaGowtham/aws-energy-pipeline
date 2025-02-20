# AWS Energy Data Pipeline - Solution & Design Decisions 🚀  

## 📌 Project Overview  
This project implements a **real-time energy data processing pipeline** using **AWS cloud services**. The system ingests energy data from various sources, processes it using AWS Lambda, and stores structured information in DynamoDB. It also provides an API to query the stored data and includes a visualization component.  

---

## **🏗️ Solution Architecture & Design Decisions**  

### 🔹 **Data Ingestion & Storage**
- **AWS S3** is used as the raw data storage layer. New data files are uploaded periodically.  
- **Trigger:** An S3 event triggers an AWS Lambda function (`process_energy_data`).  

### 🔹 **Data Processing**
- The **processing Lambda function (`process_energy_data.py`)**:
  - Reads new JSON files from S3  
  - Extracts energy generation & consumption metrics  
  - Detects anomalies (e.g., negative energy values)  
  - Stores processed data in **AWS DynamoDB**  

### 🔹 **Data Query API**
- **API Gateway** is configured to expose a public API endpoint.  
- A **query Lambda function (`query_energy_data.py`)** retrieves energy data by `site_id`.  
- The API supports **fast lookups** using DynamoDB’s `site_id` as the partition key.  

### 🔹 **Anomaly Detection & Alerting**
- If an anomaly (e.g., **negative energy values**) is detected, an **AWS SNS notification** is sent via email.  

### 🔹 **Data Visualization**
- The script **`visualize_energy_data.py`** generates insights from DynamoDB data.  
- We visualize:  
  - **Energy Trends Over Time**  
  - **Anomalies in Energy Usage**  
  - **Net Energy Trends**  

---

## **🚀 Why These Design Decisions?**
- **S3 + Lambda + DynamoDB** ensures a **serverless & scalable** architecture.  
- **Event-driven processing** (S3 → Lambda) provides **low-latency** transformations.  
- **DynamoDB** was chosen for its **fast reads & writes**, supporting real-time querying.  
- **API Gateway + Lambda** enables an efficient **serverless API** for querying data.  
- **SNS Alerts** ensure real-time notifications for energy anomalies.  

---

## **🔍 Future Enhancements**
- **Add Authentication:** Secure API access using AWS IAM or Cognito.  
- **Improve Storage Efficiency:** Optimize DynamoDB read/write capacity settings.  
- **Integrate Machine Learning:** Predict anomalies using AWS SageMaker.  

---

## **✅ Submission Details**
📌 **GitHub Repository:** [https://github.com/HarshaGowtham/aws-energy-pipeline](https://github.com/HarshaGowtham/aws-energy-pipeline)  

