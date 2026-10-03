# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    qubits = cirq.LineQubit.range(3)
    bottom_qubits = (qubits[0], qubits[1])   # control = 0, target = 1
    top_qubit = qubits[2]

    circuit = cirq.Circuit([
        cirq.CRy(0.2).on(*bottom_qubits),
        cirq.X(top_qubit),
    ])
    return circuit
