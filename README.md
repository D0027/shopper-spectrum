# 🛒 Shopper Spectrum
### Customer Segmentation & Product Recommendation Engine

---

## 🚀 Quick Setup (3 Steps)

### Step 1 — Install Python dependencies
Open your terminal / command prompt in this folder and run:
```bash
pip install -r requirements.txt
```

### Step 2 — Train the models
```bash
python train_models.py
```
This reads `data/online_retail.csv`, cleans the data, trains KMeans + builds the
cosine similarity matrix, and saves everything to the `models/` folder.
*(Takes ~1–2 minutes)*

### Step 3 — Launch the app
```bash
streamlit run app.py
```
Then open your browser at **http://localhost:8501** 🎉

---

## 📁 Project Structure
```
shopper_spectrum/
├── app.py                 ← Streamlit app (main file)
├── train_models.py        ← Model training script
├── requirements.txt       ← Python dependencies
├── data/
│   └── online_retail.csv  ← Dataset
└── models/                ← Auto-created by train_models.py
    ├── kmeans_model.pkl
    ├── scaler.pkl
    ├── label_map.pkl
    ├── item_similarity.pkl
    ├── product_list.pkl
    └── rfm_segments.csv
```

---

## 🧠 What the App Does

| Feature | Details |
|---------|---------|
| **Dashboard** | KPIs, monthly revenue trend, segment donut, top products, country analysis |
| **Product Recommendations** | Item-Based Collaborative Filtering using Cosine Similarity |
| **Customer Segmentation** | RFM → KMeans (k=4) → High-Value / Regular / Occasional / At-Risk |
| **Analytics** | Time trends, geo analysis, 3D RFM scatter, box plots |

---

## 📊 Dataset Info
- **Source:** Online Retail Dataset (UCI / Kaggle)
- **File:** `data/online_retail.csv`
- **Rows:** ~541,909 transactions
- **Columns:** InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
