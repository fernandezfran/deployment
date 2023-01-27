import feature_engine.encoding
import feature_engine.imputation
import sklearn.linear_model
import sklearn.pipeline
import sklearn.preprocessing

from model.config.core import config
from model.processing.features import ExtractLetterTransformer

titanic_pipe = sklearn.pipeline.Pipeline(
    [
        # impute categorical variables with string missing
        (
            "categorical_imputation",
            feature_engine.imputation.CategoricalImputer(
                imputation_method="missing",
                variables=config.model_config.categorical_vars,
            ),
        ),
        # add missing indicator to numerical variables
        (
            "missing_indicator",
            feature_engine.imputation.AddMissingIndicator(
                variables=config.model_config.numerical_vars
            ),
        ),
        # impute numerical variables with the median
        (
            "median_imputation",
            feature_engine.imputation.MeanMedianImputer(
                imputation_method="median", variables=config.model_config.numerical_vars
            ),
        ),
        # Extract letter from cabin
        (
            "extract_letter",
            ExtractLetterTransformer(variables=config.model_config.cabin_vars),
        ),
        # == CATEGORICAL ENCODING ======
        # remove categories present in less than 5% of the observations (0.05)
        # group them in one category called 'Rare'
        (
            "rare_label_encoder",
            feature_engine.encoding.RareLabelEncoder(
                tol=0.05, n_categories=1, variables=config.model_config.categorical_vars
            ),
        ),
        # encode categorical variables using one hot encoding into k-1 variables
        (
            "categorical_encoder",
            feature_engine.encoding.OneHotEncoder(
                drop_last=True, variables=config.model_config.categorical_vars
            ),
        ),
        # scale
        ("scaler", sklearn.preprocessing.StandardScaler()),
        ("Logit", sklearn.linear_model.LogisticRegression(C=0.0005, random_state=0)),
    ]
)
