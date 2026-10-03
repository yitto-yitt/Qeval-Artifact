# EVAL_META: task_id=70, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CSWAP(qubits[0], qubits[1], qubits[2]))
    circuit.append(cirq.H(qubits[1]))
    circuit.append((cirq.S**-1).on(qubits[0]).controlled_by(qubits[1]))
    return circuit
