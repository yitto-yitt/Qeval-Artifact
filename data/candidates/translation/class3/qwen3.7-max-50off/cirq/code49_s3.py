# EVAL_META: task_id=49, framework=cirq, class=3
import cirq

def simple_elitzur_vaidman():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.H(q0)
    ])
    return circuit
