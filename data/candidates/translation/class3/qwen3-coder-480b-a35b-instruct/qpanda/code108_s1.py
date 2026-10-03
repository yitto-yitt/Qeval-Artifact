# EVAL_META: task_id=108, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np


def initialize_adjoint_and_compose(data1, data2):
    # Convert input data to numpy arrays if they aren't already
    data1 = np.array(data1)
    data2 = np.array(data2)
    
    # Create Choi matrices from the data
    choi1 = ChoiMatrix(data1)
    choi2 = ChoiMatrix(data2)
    
    # Compute the adjoint of choi1
    adjoint_choi1 = choi1.dagger()
    
    # Compose the two Choi matrices
    composed_choi = choi1 * choi2
    
    return choi1, adjoint_choi1, composed_choi
