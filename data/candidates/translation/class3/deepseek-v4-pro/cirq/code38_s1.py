# EVAL_META: task_id=38, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.rz(theta).controlled(1)(q0, q1),
        cirq.H(q1),
        cirq.ry(theta).controlled(1)(q1, q0),
    )
    return circuit
