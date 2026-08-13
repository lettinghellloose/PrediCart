# PerdiCart

An AI-powered stock forecasting tool that helps small Kirana shops optimize inventory, predict customer demand, and automate purchasing decisions.

## 🚀 Overview

PerdiCart is an AI-powered demand forecasting and inventory planning system designed specifically for small retailers and e-grocery stores.

Instead of relying on guesswork, PerdiCart uses historical sales data, seasonal patterns, Indian festivals, holidays, weekends, and other events to forecast upcoming demand.

The system then combines the forecast with current inventory, incoming stock, and safety stock to recommend how much the retailer should purchase.

### Core Flow

Sales & Inventory Data  
↓  
Database  
↓  
LSTM Demand Forecasting  
↓  
Festival / Event / Seasonal Analysis  
↓  
Final Demand Forecast  
↓  
Inventory Analysis  
↓  
Purchase Recommendation  
↓  
Explanation  
↓  
Dashboard

## ✨ Key Features

- 📈 **AI Demand Forecasting**
  - Uses an LSTM-based model to forecast demand for the following week.
  - Learns patterns from historical sales data.

- 🪔 **Event-Aware Forecasting**
  - Considers Indian festivals, holidays, weekends, seasons, marriage seasons, and other events that can influence demand.

- 📦 **Inventory Planning**
  - Compares predicted demand against current inventory and incoming stock.

- 🛒 **Purchase Recommendations**
  - Calculates how much stock should be purchased based on forecast demand and safety stock.

- 💡 **Explainable Recommendations**
  - Explains why demand is expected to increase or decrease instead of providing only a prediction.

- 🏪 **Multi-Store Scalability**
  - Designed so the system can be extended from an individual shop to multiple retailers.

- 📊 **Interactive Dashboard**
  - Displays demand forecasts, inventory information, recommendations, trends, and explanations.

## 🧠 How It Works

### 1. Sales Data

The retailer records sales and inventory updates.

This information is stored in the database and becomes the historical foundation for forecasting.

### 2. Demand Forecasting

Historical sales are processed and provided to the LSTM forecasting model.

The model predicts the expected demand for the following week.

We use a rolling recent-history window for the forecasting model while retaining older historical data for detecting yearly and seasonal patterns.

This allows the system to benefit from recent demand trends without losing useful information such as previous years' festival demand.

### 3. Event Intelligence

The system checks upcoming events such as:

- Indian festivals
- Holidays
- Weekends
- Seasonal periods
- Marriage seasons
- Other demand-affecting events

Historical patterns around similar events can be used to provide additional context to the forecast.

For example:

> Diwali is approaching and historical sales of sweets increased significantly during previous Diwali periods.

### 4. Inventory Analysis

The forecast is compared against:

- Current stock
- Incoming stock
- Safety stock

### 5. Purchase Recommendation

The system generates a recommended purchase quantity.

The basic calculation is:

Recommended Purchase = Forecast Demand + Safety Stock - Current Stock - Incoming Stock

The result is never allowed to fall below zero.

### 6. Explanation

Instead of returning only:

> Expected demand: 145 units

PerdiCart provides context such as:

> Expected demand: 145 units (+35%)  
> Why: Diwali is approaching, historical Diwali demand was higher, and recent sales are trending upward.

This makes the recommendation easier for a shopkeeper to understand and act upon.

## 🏗️ Architecture

```text
                    React Dashboard
                           │
                           │ HTTP / JSON
                           ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    │   Backend    │
                    └──────┬───────┘
                           │
          ┌────────────────┼─────────────────┐
          ▼                ▼                 ▼
      SQLite          ML Pipeline       Event Engine
          │                │                 │
          │              LSTM                │
          │                │                 │
          └────────────────┼─────────────────┘
                           ▼
                 Recommendation Engine
                           │
                           ▼
                    Explanation Engine
                           │
                           ▼
                    JSON Response
                           │
                           ▼
                    React Dashboard
