# EVAL_META: task_id=118, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import *


def create_c3sx_circuit():
    machine = CPUQVM()
    if hasattr(machine, "init"):
        machine.init()

    q = machine.qAlloc_many(4)
    circuit = QCircuit()

    sx_gate = globals().get("SX", None)
    if sx_gate is not None:
        circuit << sx_gate(q[3]).control([q[0], q[1], q[2]])
    else:
        phase_gate = globals().get("P", None)
        if phase_gate is None:
            phase_gate = globals().get("U1")
        circuit << phase_gate(q[2], pi / 4).control([q[0], q[1]])
        circuit << RX(q[3], pi / 2).control([q[0], q[1], q[2]])

    create_c3sx_circuit._machine = machine
    create_c3sx_circuit._qubits = q
    return circuit
