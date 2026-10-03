# EVAL_META: task_id=49, framework=cirq, class=3
import cirq

def simple_elitzur_vaidman():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(q[0]),
        cirq.CNOT(q[0], q[1]),
        cirq.H(q[0]),
    ])
    return circuit
