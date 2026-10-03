# EVAL_META: task_id=71, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_csx01_h1():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append((cirq.X ** 0.5).controlled().on(qubits[0], qubits[1]))
    circuit.append(cirq.H(qubits[1]))
    return circuit
