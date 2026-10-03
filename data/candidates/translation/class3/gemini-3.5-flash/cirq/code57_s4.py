# EVAL_META: task_id=57, framework=cirq, class=3
import cirq

def create_swap_gate():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.CNOT(qubits[1], qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    return circuit
