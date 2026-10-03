# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def custom_rotation_gate():
    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(1)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(1)
    elif hasattr(machine, "qAlloc"):
        qubits = [machine.qAlloc()]
    else:
        qubits = [machine.qalloc()]

    circuit = QCircuit()
    angle = float(np.pi / 2)
    gate = U3(qubits[0], angle, angle, angle)

    try:
        updated = circuit << gate
        if updated is not None:
            circuit = updated
    except Exception:
        circuit.insert(gate)

    global _custom_rotation_gate_resources
    _custom_rotation_gate_resources = (machine, qubits)
    return circuit
