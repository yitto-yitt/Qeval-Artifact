# EVAL_META: task_id=66, framework=cirq, class=2
import cirq
from numpy import arccos, sqrt


def w_state():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    theta = 2 * arccos(1 / sqrt(3))
    circuit.append(cirq.Ry(rads=theta).on(qubits[0]))
    circuit.append(cirq.H.controlled(1).on(qubits[0], qubits[1]))
    circuit.append(cirq.CNOT.on(qubits[1], qubits[2]))
    circuit.append(cirq.CNOT.on(qubits[0], qubits[1]))
    circuit.append(cirq.X.on(qubits[0]))
    circuit.append(cirq.measure(*qubits, key="result"))
    return circuit
