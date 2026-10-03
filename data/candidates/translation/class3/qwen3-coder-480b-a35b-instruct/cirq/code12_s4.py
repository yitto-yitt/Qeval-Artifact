# EVAL_META: task_id=12, framework=cirq, class=3
import cirq
import numpy as np


def get_unitary():
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    unitary = circuit.unitary(qubit_order=qubits)
    return unitary
