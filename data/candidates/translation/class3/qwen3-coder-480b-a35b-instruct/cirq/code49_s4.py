# EVAL_META: task_id=49, framework=cirq, class=3
import cirq

def simple_elitzur_vaidman():
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.H(qubits[0]))
    return circuit
