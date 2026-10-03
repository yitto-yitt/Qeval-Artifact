# EVAL_META: task_id=49, framework=cirq, class=3
import cirq

def simple_elitzur_vaidman():
    qubit0 = cirq.LineQubit(0)
    qubit1 = cirq.LineQubit(1)
    circuit = cirq.Circuit([
        cirq.H(qubit0),
        cirq.CX(qubit0, qubit1),
        cirq.H(qubit0),
    ])
    return circuit
