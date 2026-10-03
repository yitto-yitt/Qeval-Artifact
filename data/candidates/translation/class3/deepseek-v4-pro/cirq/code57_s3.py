# EVAL_META: task_id=57, framework=cirq, class=3
import cirq

def create_swap_gate():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.CX(q0, q1),
        cirq.CX(q1, q0),
        cirq.CX(q0, q1),
    ])
    return circuit
