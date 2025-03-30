import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans


df = pd.read_csv("/Users/faitusjelinejoseph/Documents/Project/formatted_data.csv")


df['county'] = df['county'].fillna('Unknown') 


df['county'] = LabelEncoder().fit_transform(df['county'].astype(str))

# Calculate age and handle missing birth dates
df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")
df["age"] = 2025 - df["date_of_birth"].dt.year

# Impute missing ages with median
age_imputer = SimpleImputer(strategy='median')
df["age"] = age_imputer.fit_transform(df[["age"]])


X = df[['age', 'county']].dropna()

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Elbow Method
wcss = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Plot Elbow Curve
plt.figure(figsize=(10, 6))
plt.plot(k_range, wcss, marker='o', linestyle='--')
plt.title('Elbow Method (Age + County Clustering)')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WCSS')
plt.xticks(k_range)
plt.grid()
plt.show()

# Determine optimal k (using second derivative method)
diffs = np.diff(wcss)
diff_ratios = diffs[:-1] / diffs[1:]
optimal_k = np.argmax(diff_ratios) + 2 

print(f"Optimal number of clusters: {optimal_k}")

# Final Clustering
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Visualization
plt.figure(figsize=(10, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap='viridis', alpha=0.6)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            s=300, c='red', marker='X', label='Centroids')
plt.title(f'Age vs County Clusters (k={optimal_k})')
plt.xlabel('Standardized Age')
plt.ylabel('Encoded County')
plt.colorbar(label='Cluster')
plt.legend()
plt.grid()
plt.show()