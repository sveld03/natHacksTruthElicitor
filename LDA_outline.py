
labels = np.array([labels == 2], dtype=int)[0]

X = np.vstack((red_cum_signals, yel_cum_signals, blu_cum_signals))
y = labels

shuffled_indices = np.arange(3*ntrials)
np.random.shuffle(shuffled_indices)

train_indices = shuffled_indices[:240]
test_indices = shuffled_indices[240:]

X_train, y_train = X[train_indices], y[train_indices]
X_test, y_test = X[test_indices], y[test_indices]

clf = LDA()
clf.fit(X_train, y_train)
print(f'Score: {clf.score(X_test, y_test)}')