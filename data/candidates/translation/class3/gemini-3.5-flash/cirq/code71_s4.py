# EVAL_META: task_id=71, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_csx01_h1():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append((cirq.X**0.5).on(qubits[1]).controlled_by(qubits[0]))
    circuit.append(cirq.H(qubits[1]))
    return circuit
