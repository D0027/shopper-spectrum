"""
train_models.py
Run this once before launching the Streamlit app.
  python train_models.py
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import joblib, pickle, os

print("=" * 55)
print("  Shopper Spectrum — Model Training")
print("=" * 55)

# ── 1. Load & Clean ──────────────────────────────────────────
print("\n📂 Loading dataset...")
df = pd.read_csv("data/online_retail.csv", encoding="latin1")
print(f"   Raw rows: {len(df):,}")

df = df.dropna(subset=["CustomerID"])
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]
df = df.drop_duplicates()
df["InvoiceDate"]  = pd.to_datetime(df["InvoiceDate"])
df["CustomerID"]   = df["CustomerID"].astype(int)
df["TotalAmount"]  = df["Quantity"] * df["UnitPrice"]
print(f"   Clean rows: {len(df):,}")

# ── 2. RFM Feature Engineering ───────────────────────────────
print("\n🧮 Computing RFM features...")
reference_date = df["InvoiceDate"].max()
rfm = df.groupby("CustomerID").agg(
    Recency   = ("InvoiceDate", lambda x: (reference_date - x.max()).days),
    Frequency = ("InvoiceNo",   "nunique"),
    Monetary  = ("TotalAmount", "sum")
).reset_index()
print(f"   Customers: {len(rfm):,}")

# ── 3. Scale ─────────────────────────────────────────────────
print("\n⚙️  Scaling features...")
rfm_log = rfm[["Recency","Frequency","Monetary"]].copy()
for c in rfm_log.columns:
    rfm_log[c] = np.log1p(rfm_log[c])

scaler    = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_log)

# ── 4. KMeans ────────────────────────────────────────────────
print("\n🤖 Training KMeans (k=4)...")
kmeans = KMeans(n_clusters=4, init="k-means++", n_init=15, random_state=42)
rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)
print(f"   Inertia: {kmeans.inertia_:,.2f}")

# ── 5. Auto-label clusters ───────────────────────────────────
profile = rfm.groupby("Cluster").agg(
    R=("Recency","mean"), F=("Frequency","mean"), M=("Monetary","mean"))
profile["Score"] = (profile["R"].rank(ascending=True) +
                    profile["F"].rank(ascending=False) +
                    profile["M"].rank(ascending=False))
sorted_c  = profile.sort_values("Score").index.tolist()
labels    = ["High-Value", "Regular", "Occasional", "At-Risk"]
label_map = {c: labels[i] for i, c in enumerate(sorted_c)}
rfm["Segment"] = rfm["Cluster"].map(label_map)

print("\n   Segments:")
for seg, cnt in rfm["Segment"].value_counts().items():
    print(f"   • {seg}: {cnt:,} customers")

# ── 6. Recommendation matrix ─────────────────────────────────
print("\n🔗 Building item similarity matrix...")
prod_freq = df.groupby("Description")["InvoiceNo"].nunique()
popular   = prod_freq[prod_freq >= 10].index
basket    = (df[df["Description"].isin(popular)]
             .groupby(["CustomerID","Description"])["Quantity"].sum().reset_index())
matrix    = basket.pivot_table(index="CustomerID", columns="Description",
                                values="Quantity", fill_value=0)
item_sim  = cosine_similarity(matrix.T)
item_sim_df = pd.DataFrame(item_sim, index=matrix.columns, columns=matrix.columns)
print(f"   Products in matrix: {item_sim_df.shape[0]:,}")

# ── 7. Save ──────────────────────────────────────────────────
print("\n💾 Saving models...")
os.makedirs("models", exist_ok=True)
joblib.dump(kmeans,    "models/kmeans_model.pkl")
joblib.dump(scaler,    "models/scaler.pkl")
with open("models/label_map.pkl","wb")    as f: pickle.dump(label_map, f)
with open("models/product_list.pkl","wb") as f: pickle.dump(item_sim_df.index.tolist(), f)
item_sim_df.to_pickle("models/item_similarity.pkl")
rfm[["CustomerID","Recency","Frequency","Monetary","Segment"]].to_csv(
    "models/rfm_segments.csv", index=False)

print("\n✅ All models saved to models/")
print("=" * 55)
print("  Run:  streamlit run app.py")
print("=" * 55)
