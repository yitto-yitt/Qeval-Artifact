# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import *
import math

def qft_inverse(n):
    try:
        circuit = QCircuit(n)
    except TypeError:
        circuit = QCircuit()

    qubits = list(range(n))

    def append_gate(gate):
        try:
            circuit << gate
        except TypeError:
            circuit.insert(gate)

    def controlled_phase(control, target, angle):
        if "CP" in globals():
            try:
                return CP(control, target, angle)
            except TypeError:
                try:
                    return CP(angle, control, target)
                except TypeError:
                    pass
        if "CR" in globals():
            try:
                return CR(control, target, angle)
            except TypeError:
                try:
                    return CR(angle, control, target)
                except TypeError:
                    pass
        if "P" in globals():
            gate = P(target, angle)
            try:
                return gate.control([control])
            except TypeError:
                return gate.control(control)
        gate = U1(target, angle)
        try:
            return gate.control([control])
        except TypeError:
            return gate.control(control)

    for i in range(n // 2):
        append_gate(SWAP(qubits[i], qubits[n - i - 1]))

    for target in range(n):
        for control in range(target):
            angle = -math.pi / (2 ** (target - control))
            append_gate(controlled_phase(qubits[control], qubits[target], angle))
        append_gate(H(qubits[target]))

    return circuit
