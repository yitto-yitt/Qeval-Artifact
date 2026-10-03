# EVAL_META: task_id=2, framework=cirq, class=2
import cirq
import numpy as np


def create_bell_statevector():
    # Create the |00⟩ and |11⟩ states
    zero_zero = np.array([1, 0, 0, 0], dtype=complex)  # |00⟩
    one_one = np.array([0, 0, 0, 1], dtype=complex)    # |11⟩
    
    # Create the Phi+ Bell state: (|00⟩ + |11⟩) / sqrt(2)
    bell_state = (zero_zero + one_one) / np.sqrt(2)
    
    # Return as a numpy array representing the state vector
    return bell_state
