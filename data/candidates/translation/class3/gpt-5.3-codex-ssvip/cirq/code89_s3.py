# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    cch = cirq.H.controlled(num_controls=2)
    circuit.append(cch(q0, q1, q2))
    return circuit
