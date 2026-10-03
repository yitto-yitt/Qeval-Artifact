# EVAL_META: task_id=11, framework=cirq, class=2
import cirq

def get_statevector(circuit):
    result = cirq.Simulator().simulate(circuit)
    return result.final_state_vector
