# EVAL_META: task_id=66, framework=cirq, class=2
from numpy import arccos, sqrt
import cirq


def w_state():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    theta = 2 * arccos(1 / sqrt(3))
    circuit.append(cirq.Ry(rads=theta).on(qubits[0]))
    circuit.append(cirq.H(qubits[1]).controlled_by(qubits[0]))
    circuit.append(cirq.CNOT(qubits[1], qubits[2]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.X(qubits[0]))
    circuit.append(cirq.measure(*qubits, key='m'))
    return circuit
