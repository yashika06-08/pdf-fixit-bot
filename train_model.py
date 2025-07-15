
# train_model.py
import joblib
from sklearn.linear_model import LogisticRegression

# Dummy training data
X = [[5], [100], [10], [250], [15]]  # Example feature: text length
y = ['blank', 'content', 'blank', 'chapter', 'blank']

# Train a simple model
model = LogisticRegression()
model.fit(X, y)

# Save the model to models/page_classifier.pkl
joblib.dump(model, 'models/page_classifier.pkl')
print("✅ Model saved to models/page_classifier.pkl")
