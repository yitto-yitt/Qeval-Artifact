# EVAL_META: task_id=59, framework=cirq, class=3
import cirq

def create_cz_gate():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(q1),
        cirq.CNOT(q0, q1),
        cirq.H(q1)
    ])
    return circuit
