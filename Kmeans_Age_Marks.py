import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans

# Load dataset
df = pd.read_csv("/Users/faitusjelinejoseph/Documents/Project/train.csv")

# Selecting relevant features (assuming 'Age' and 'Marks' are numeric)
X = df[['Age', 'Marks']]

# Handling missing values if any
imputer = SimpleImputer(strategy="mean")
X = imputer.fit_transform(X)

# Standardizing the data for better clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Finding the optimal number of clusters using the Elbow method
wcss = []
K_range = range(1, 11)  # Testing k from 1 to 10

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)  # Sum of squared distances to closest centroid

# Plotting the elbow curve
plt.figure(figsize=(8, 5))
plt.plot(K_range, wcss, marker='o', linestyle='--')
plt.xlabel("Number of Clusters (k)")
plt.ylabel("WCSS (Within-Cluster Sum of Squares)")
plt.title("Elbow Method to Determine Optimal k")
plt.show()

kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# Visualization
plt.figure(figsize=(10, 6))

# Scatter plot of clustered data
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap='viridis', alpha=0.6, edgecolors='k')

# Plot cluster centroids
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            s=300, c='red', marker='X', label='Centroids')

# Labels and title
plt.title(f'Age vs Marks Clusters (k={3})')
plt.xlabel('Standardized Age')
plt.ylabel('Standardized Marks')
plt.colorbar(label='Cluster')
plt.legend()
plt.grid(True)

# Show plot
plt.show()
