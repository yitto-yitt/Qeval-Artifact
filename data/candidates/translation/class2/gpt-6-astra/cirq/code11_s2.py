# EVAL_META: task_id=11, framework=cirq, class=2
import cirq
import numpy as np

def get_statevector(circuit):
    return cirq.Simulator(dtype=np.complex128).simulate(circuit).final_state_vector
