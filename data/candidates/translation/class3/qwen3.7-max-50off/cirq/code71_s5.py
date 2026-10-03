# EVAL_META: task_id=71, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_csx01_h1():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit([
        cirq.H(q0),
        cirq.CSX(q0, q1),
        cirq.H(q1)
    ])
    return circuit
