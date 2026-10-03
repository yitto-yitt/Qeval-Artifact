# EVAL_META: task_id=66, framework=cirq, class=2
from numpy import arccos, sqrt
import cirq

def w_state():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.ry(2 * arccos(1 / sqrt(3))).on(qubits[0]),
        cirq.H.controlled().on(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.X(qubits[0]),
        cirq.measure(*qubits, key='result')
    )
    return circuit
