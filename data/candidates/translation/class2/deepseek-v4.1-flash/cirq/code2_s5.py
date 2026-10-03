# EVAL_META: task_id=2, framework=cirq, class=2
import cirq
import numpy as np

def create_bell_statevector():
    return cirq.to_valid_state_vector(
        np.array([1, 0, 0, 1], dtype=np.complex128) / np.sqrt(2),
        qid_shape=(2, 2)
    )
