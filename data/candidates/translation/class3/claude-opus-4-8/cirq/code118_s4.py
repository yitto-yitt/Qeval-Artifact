# EVAL_META: task_id=118, framework=cirq, class=3
import cirq
import numpy as np


def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    sx_gate = cirq.XPowGate(exponent=0.5)
    c3sx = sx_gate.controlled(num_controls=3)
    circuit = cirq.Circuit()
    circuit.append(c3sx.on(qubits[0], qubits[1], qubits[2], qubits[3]))
    return circuit
