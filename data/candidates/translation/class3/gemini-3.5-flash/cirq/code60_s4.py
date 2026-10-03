# EVAL_META: task_id=60, framework=cirq, class=3
import cirq

def create_cy_gate():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.inverse(cirq.S)(qubits[1]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.S(qubits[1]))
    return circuit
