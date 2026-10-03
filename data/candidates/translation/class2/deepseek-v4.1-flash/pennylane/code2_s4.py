# EVAL_META: task_id=2, framework=pennylane, class=2
import numpy as np

def create_bell_statevector():
    state_00 = np.zeros(4)
    state_00[0] = 1
    state_11 = np.zeros(4)
    state_11[3] = 1
    return (state_00 + state_11) / np.sqrt(2)
