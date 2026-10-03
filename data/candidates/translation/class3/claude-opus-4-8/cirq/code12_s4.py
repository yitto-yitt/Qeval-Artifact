# EVAL_META: task_id=12, framework=cirq, class=3
import cirq
import numpy as np


def get_unitary():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    return circuit.unitary(qubit_order=[q1, q0])
