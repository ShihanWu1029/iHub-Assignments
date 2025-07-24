# -------------------------------------------------
# 1. Imports
# -------------------------------------------------
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# -------------------------------------------------
# 2. Load data (Wine data set – 3 classes, 178 samples)
# -------------------------------------------------
wine = datasets.load_wine()
X, y = wine.data, wine.target

# -------------------------------------------------
# 3. Train / test split (stratified to keep class proportions)
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# -------------------------------------------------
# 4. Build pipeline: scaling → SVM
# -------------------------------------------------
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('svc',    SVC())
])

# -------------------------------------------------
# 5. Hyper-parameter grid (RBF kernel)
# -------------------------------------------------
param_grid = {
    'svc__kernel': ['rbf'],
    'svc__C':      [0.1, 1, 10, 100],
    'svc__gamma':  ['scale', 0.01, 0.1, 1]
}

# -------------------------------------------------
# 6. Grid-search with 5-fold CV on the training data
# -------------------------------------------------
grid = GridSearchCV(
    pipe,
    param_grid=param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)
grid.fit(X_train, y_train)

print("Best CV accuracy : {:.3f}".format(grid.best_score_))
print("Best parameters  : ", grid.best_params_)

# -------------------------------------------------
# 7. Evaluate on the held-out test set
# -------------------------------------------------
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)

print("\nConfusion matrix (test set):")
print(confusion_matrix(y_test, y_pred))

print("\nClassification report (test set):")
print(classification_report(y_test, y_pred))

print("Overall accuracy on test set: {:.3f}".format(
    accuracy_score(y_test, y_pred)
))