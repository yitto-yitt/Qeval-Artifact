# EVAL_META: task_id=38, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append((cirq.rz(theta).controlled_by(q0)).on(q1))
    circuit.append(cirq.H(q1))
    circuit.append((cirq.ry(theta).controlled_by(q1)).on(q0))
    return circuit
