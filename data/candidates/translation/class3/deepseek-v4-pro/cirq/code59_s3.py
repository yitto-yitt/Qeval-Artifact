# EVAL_META: task_id=59, framework=cirq, class=3
import cirq

def create_cz_gate():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.H(qubits[1]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.H(qubits[1]),
    ])
    return circuit
