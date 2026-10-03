# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    q = cirq.LineQubit.range(3)
    gate = cirq.H.controlled(2)
    circuit = cirq.Circuit(gate(*q))
    return circuit
