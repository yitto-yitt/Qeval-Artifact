# EVAL_META: task_id=3, framework=cirq, class=2
import cirq


def create_ghz(drawing=False):
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.CNOT(qubits[0], qubits[2]))
    
    # Add measurements
    circuit.append(cirq.measure(*qubits, key='result'))
    
    if drawing:
        return circuit, circuit.to_text_diagram()
    return circuit
