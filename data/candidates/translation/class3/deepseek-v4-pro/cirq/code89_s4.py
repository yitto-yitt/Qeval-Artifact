# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    q0, q1, q2 = cirq.LineQubit.range(3)
    gate = cirq.H.controlled(2)
    circuit = cirq.Circuit(gate.on(q0, q1, q2))
    return circuit
