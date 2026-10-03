# EVAL_META: task_id=38, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)

    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.rz(theta)(q1).controlled_by(q0))
    circuit.append(cirq.H(q1))
    circuit.append(cirq.ry(theta)(q0).controlled_by(q1))

    return circuit
