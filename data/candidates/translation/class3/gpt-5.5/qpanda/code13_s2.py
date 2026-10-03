# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def custom_rotation_gate():
    theta = float(np.pi / 2)
    phi = float(np.pi / 2)
    lam = float(np.pi / 2)

    def _new_circuit():
        try:
            return QCircuit(1)
        except Exception:
            return QCircuit()

    def _append_u(circuit, qubit):
        if "U3" in globals():
            circuit << U3(qubit, theta, phi, lam)
        elif "U" in globals():
            circuit << U(qubit, theta, phi, lam)
        else:
            circuit << RZ(qubit, phi)
            circuit << RY(qubit, theta)
            circuit << RZ(qubit, lam)

    circuit = _new_circuit()
    try:
        _append_u(circuit, 0)
        return circuit
    except Exception:
        pass

    qvm = CPUQVM()
    for init_name in ("init_qvm", "init"):
        init_method = getattr(qvm, init_name, None)
        if callable(init_method):
            init_method()
            break

    qubits = qvm.qAlloc_many(1)
    circuit = _new_circuit()
    _append_u(circuit, qubits[0])

    resources = getattr(custom_rotation_gate, "_resources", [])
    resources.append((qvm, qubits))
    custom_rotation_gate._resources = resources

    return circuit
