# EVAL_META: task_id=118, framework=cirq, class=3
import cirq
import numpy as np


def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    sx = cirq.XPowGate(exponent=0.5)
    controlled_sx = sx.controlled(num_controls=3)
    circuit = cirq.Circuit()
    circuit.append(controlled_sx.on(qubits[0], qubits[1], qubits[2], qubits[3]))
    return circuit
