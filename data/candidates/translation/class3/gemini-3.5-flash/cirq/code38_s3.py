# EVAL_META: task_id=38, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.rz(theta).on(qubits[1]).controlled_by(qubits[0]))
    circuit.append(cirq.H(qubits[1]))
    circuit.append(cirq.ry(theta).on(qubits[0]).controlled_by(qubits[1]))
    return circuit
