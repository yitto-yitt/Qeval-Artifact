# EVAL_META: task_id=145, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import *

def qft_inverse(n):
    n = int(n)

    try:
        circuit = QCircuit(n)
    except Exception:
        circuit = QCircuit()

    qubits = list(range(n))

    def _append(cir, op):
        try:
            res = cir << op
            return cir if res is None else res
        except Exception:
            res = cir.insert(op)
            return cir if res is None else res

    def _append_controlled_phase(cir, control, target, angle):
        for gate_name in ("CP", "CR", "CPHASE"):
            gate_fn = globals().get(gate_name)
            if gate_fn is not None:
                try:
                    return _append(cir, gate_fn(control, target, angle))
                except Exception:
                    pass

        cir = _append(cir, RZ(control, angle / 2.0))
        cir = _append(cir, CNOT(control, target))
        cir = _append(cir, RZ(target, -angle / 2.0))
        cir = _append(cir, CNOT(control, target))
        cir = _append(cir, RZ(target, angle / 2.0))
        return cir

    for i in range(n // 2):
        a = qubits[i]
        b = qubits[n - i - 1]
        circuit = _append(circuit, CNOT(a, b))
        circuit = _append(circuit, CNOT(b, a))
        circuit = _append(circuit, CNOT(a, b))

    for j in range(n):
        for m in range(j):
            circuit = _append_controlled_phase(
                circuit,
                qubits[m],
                qubits[j],
                -pi / (2 ** (j - m)),
            )
        circuit = _append(circuit, H(qubits[j]))

    return circuit
