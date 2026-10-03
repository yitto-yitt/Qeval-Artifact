# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    q = cirq.LineQubit.range(3)
    c3h_gate = cirq.H.controlled(num_controls=2)
    circuit = cirq.Circuit(c3h_gate.on(*q))
    return circuit
