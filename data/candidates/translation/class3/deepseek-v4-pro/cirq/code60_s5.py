# EVAL_META: task_id=60, framework=cirq, class=3
import cirq

def create_cy_gate():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit([
        cirq.S(qubits[1]) ** -1,
        cirq.CX(qubits[0], qubits[1]),
        cirq.S(qubits[1]),
    ])
    return circuit
