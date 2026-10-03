# EVAL_META: task_id=71, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_csx01_h1():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.H(qubits[2]))  # Hadamard on control qubit (qubit 0)
    circuit.append(cirq.H(qubits[1]) ** 0.5)  # Sqrt(X) on target qubit (qubit 1)
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.H(qubits[2]))  # Hadamard on control qubit again to revert
    circuit.append(cirq.H(qubits[1]) ** -0.5)  # Inverse Sqrt(X) on target qubit
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.H(qubits[1]))
    return circuit
