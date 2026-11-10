from sklearn.ensemble import RandomForestRegressor

from src.models.supervised_model import SupervisedTimeSeriesModel

class RandomForestModel(SupervisedTimeSeriesModel):
    def __init__(
        self,
        n_estimators=300,
        max_depth=5,
        min_samples_leaf=2,
        random_state=42
    ):
        super().__init__('RandomForest')

        self.estimator = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state,
            n_jobs=-1
        )