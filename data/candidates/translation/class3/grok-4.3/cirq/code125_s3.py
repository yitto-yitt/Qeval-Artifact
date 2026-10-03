# EVAL_META: task_id=125, framework=cirq, class=3
import cirq

def circ_to_gate(circ):
    circ_gate = cirq.CircuitOperation(circ.freeze())
    return circ_gate
