# EVAL_META: task_id=130, framework=cirq, class=3
import cirq

def inv_circuit(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[1]))
    circuit.append(cirq.H(qubits[2]))
    circuit.append(cirq.CX(qubits[1], qubits[3]))
    circuit.append(cirq.CX(qubits[2], qubits[4]))
    return cirq.inverse(circuit)
