# Ported from: https://github.com/ProgBelarus/BatchMultivalidConformal/tree/main/src/CalibrationScorers
from abc import ABC, abstractmethod
import numpy as np

class PredictionSet(ABC):
    @abstractmethod
    def cover(self, y):
        pass
    
    @abstractmethod
    def get_size(self):
        pass 

class CalibrationScorer(ABC):
    @abstractmethod
    def calc_score(self, x, y):
        pass

    @abstractmethod
    def get_prediction_set(self, x, calibration_score):
        pass

class customResidualCalibrationPredictionSet(PredictionSet):
    def __init__(self, interval_center, interval_width):
        self.interval_center = interval_center
        self.interval_width = interval_width
        # The width calculated using our interval will always be bounded above by one
        # To allow for larger intervals, we introduce this factor which stretches the interval
        # by the desired amount. 

    def cover(self, y):
        return self.interval_center -  self.interval_width <= y < self.interval_center + self.interval_width
    
    def get_size(self):
        return 2 * self.interval_width


class customResidualCalibrationScorer(CalibrationScorer):
    def __init__(self, width_mult_factor):
        self.f_pred = None
        self.width_mult_factor = width_mult_factor

    def calc_score(self, x, y):
        return (1 / self.width_mult_factor) * np.abs(y - self.f_pred(x))

    def get_prediction_set(self, x, calibration_threshold, width_mult_factor):
        interval_center = self.f_pred(x)
        interval_width = width_mult_factor * calibration_threshold
        new_prediction_set = customResidualCalibrationPredictionSet(interval_center, interval_width)
        return new_prediction_set

    def update(self, f_pred):
        self.f_pred = f_pred