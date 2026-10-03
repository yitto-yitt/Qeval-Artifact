# EVAL_META: task_id=11, framework=cirq, class=2
import cirq
import numpy as np

def get_statevector(circuit):
    return cirq.final_state_vector(circuit, initial_state=0, dtype=np.complex128)
