# EVAL_META: task_id=38, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.Rz(theta).controlled().on(q0, q1))
    circuit.append(cirq.H(q1))
    circuit.append(cirq.Ry(theta).controlled().on(q1, q0))
    return circuit
