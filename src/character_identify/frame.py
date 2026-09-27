from dataclasses import dataclass

import numpy as np

@dataclass
class Frame:
    id: int
    timestamp: float
    image: np.ndarray