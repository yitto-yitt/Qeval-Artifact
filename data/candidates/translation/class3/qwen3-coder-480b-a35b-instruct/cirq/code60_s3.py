# EVAL_META: task_id=60, framework=cirq, class=3
import cirq

def create_cy_gate():
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    circuit = cirq.Circuit()
    circuit.append(cirq.S(qubits[1]).inv())
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.S(qubits[1]))
    return circuit
