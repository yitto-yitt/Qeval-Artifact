# EVAL_META: task_id=41, framework=cirq, class=3
import cirq


def compose_op():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.X(qubits[0]),
        cirq.I(qubits[1]),
        cirq.Y(qubits[2]),
    )
    return cirq.MatrixGate(circuit.unitary(qubit_order=qubits[::-1]))
