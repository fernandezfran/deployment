import sklearn.base


class ExtractLetterTransformer(
    sklearn.base.BaseEstimator, sklearn.base.TransformerMixin
):
    """Extract the first letter of the variable."""

    def __init__(self, variables):
        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X, y=None):
        """Not used but necessary for the sklearn pipeline"""
        return self

    def transform(self, X):
        """Perform the extraction of the first letter"""
        X = X.copy()

        for feature in self.variables:
            X[feature] = X[feature].str[0]

        return X
