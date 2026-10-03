# EVAL_META: task_id=69, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.S(qubits[1]).controlled_by(qubits[0]))
    circuit.append(cirq.H(qubits[1]))
    circuit.append((cirq.S**-1)(qubits[0]).controlled_by(qubits[1]))
    return circuit
