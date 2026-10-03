# EVAL_META: task_id=11, framework=cirq, class=2
import cirq

def get_statevector(circuit):
    return cirq.final_state_vector(circuit)
