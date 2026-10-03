# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def custom_rotation_gate():
    theta = np.pi / 2
    phi = np.pi / 2
    lam = np.pi / 2

    machine = CPUQVM()
    for method_name in ("init", "init_qvm"):
        if hasattr(machine, method_name):
            getattr(machine, method_name)()
            break

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(1)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(1)
    elif hasattr(machine, "q_alloc_many"):
        qubits = machine.q_alloc_many(1)
    elif hasattr(machine, "qAlloc"):
        qubits = [machine.qAlloc()]
    elif hasattr(machine, "qalloc"):
        qubits = [machine.qalloc()]
    else:
        qubits = [machine.q_alloc()]

    circuit = QCircuit() if "QCircuit" in globals() else QProg()

    gate = None
    for gate_name, arg_lists in (
        ("U3", ((qubits[0], theta, phi, lam), (theta, phi, lam, qubits[0]))),
        ("U", ((qubits[0], theta, phi, lam), (theta, phi, lam, qubits[0]))),
        ("U4", ((qubits[0], theta, phi, lam, 0.0), (theta, phi, lam, 0.0, qubits[0]))),
    ):
        gate_ctor = globals().get(gate_name)
        if gate_ctor is None:
            continue
        for args in arg_lists:
            try:
                gate = gate_ctor(*args)
                break
            except TypeError:
                continue
        if gate is not None:
            break

    if gate is not None:
        circuit << gate
    else:
        circuit << RZ(qubits[0], lam) << RY(qubits[0], theta) << RZ(qubits[0], phi)

    custom_rotation_gate._machine = machine
    custom_rotation_gate._qubits = qubits
    return circuit
