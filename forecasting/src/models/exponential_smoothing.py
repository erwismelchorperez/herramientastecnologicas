import warnings
import numpy as np
import pandas as pd

from statsmodels.tsa.holtwinters import (
    ExponentialSmoothing as StatsmodelsES
)
from statsmodels.tools.sm_exceptions import ConvergenceWarning

from src.models.base_model import BaseModel


class ExponentialSmoothingModel(BaseModel):

    def __init__(
        self,
        trend=None,
        seasonal=None,
        seasonal_periods=None,
        damped_trend=False,
        maxiter=2000
    ):
        name = f"ExponentialSmoothing_{trend}_{seasonal}_{damped_trend}"
        super().__init__(name)

        self.trend = trend
        self.seasonal = seasonal
        self.seasonal_periods = seasonal_periods
        self.damped_trend = damped_trend
        self.maxiter = maxiter

        self.model = None
        self.fitted_model = None

        self.training_diagnostics_ = {}

    def _fit_with_optimizer(self, method, use_brute=True):

        with warnings.catch_warnings(record=True) as captured:

            warnings.simplefilter("always")

            fitted = self.model.fit(
                optimized=True,
                method=method,
                use_brute=use_brute,
                minimize_kwargs={
                    'options': {
                        'maxiter': self.maxiter
                    }
                }
            )

        convergence_warnings = [
            str(w.message)
            for w in captured
            if issubclass(w.category, ConvergenceWarning)
        ]

        retvals = getattr(fitted, 'mle_retvals', {}) or {}

        success = retvals.get(
            'success',
            len(convergence_warnings) == 0
        )

        forecast_check = np.asarray(
            fitted.forecast(1),
            dtype=float
        )

        valid_forecast = np.isfinite(forecast_check).all()

        return {
            'fitted_model': fitted,
            'success': bool(success) and valid_forecast,
            'method': method,
            'message': retvals.get('message', ''),
            'iterations': retvals.get('nit'),
            'objective': retvals.get('fun', retvals.get('fopt')),
            'warnings': convergence_warnings
        }

    def fit(self, series):

        self.series = self._prepare_series(series)
        self.last_date = self.series.index[-1]

        self.model = StatsmodelsES(
            self.series,
            trend=self.trend,
            damped_trend=self.damped_trend,
            seasonal=self.seasonal,
            seasonal_periods=self.seasonal_periods,
            initialization_method='estimated'
        )

        # Estrategias de optimización
        optimizers = [
            ('L-BFGS-B', True),
            ('Powell', False)
        ]

        attempts = []
        successful_result = None

        for method, use_brute in optimizers:

            result = self._fit_with_optimizer(
                method=method,
                use_brute=use_brute
            )

            attempts.append({
                'method': result['method'],
                'success': result['success'],
                'message': str(result['message']),
                'iterations': result['iterations'],
                'objective': result['objective'],
                'warnings': result['warnings']
            })

            print(
                f"Optimizador: {method} | "
                f"Convergencia: {result['success']}"
            )

            if result['success']:
                successful_result = result
                break

        if successful_result is None:

            self.training_diagnostics_ = {
                'converged': False,
                'attempts': attempts
            }

            raise RuntimeError(
                "No fue posible obtener una solución convergente "
                "para Exponential Smoothing. "
                f"Intentos: {attempts}"
            )

        self.fitted_model = successful_result['fitted_model']

        self.training_diagnostics_ = {
            'converged': True,
            'optimizer': successful_result['method'],
            'iterations': successful_result['iterations'],
            'objective': successful_result['objective'],
            'message': str(successful_result['message']),
            'attempts': attempts
        }

        self.is_fitted = True

        return self

    def predict(self, steps):

        self._validate_steps(steps)

        values = self.fitted_model.forecast(steps)

        return pd.Series(
            values.to_numpy(),
            index=self._future_index(steps),
            name='forecast'
        )