# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import *


def bv_function(s):
    n = len(s)

    def _append(circuit, gate):
        try:
            circuit << gate
        except Exception:
            circuit.insert(gate)
        return circuit

    try:
        qc = QCircuit(n + 1)
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                _append(qc, CNOT(index, n))
        return qc
    except Exception:
        qvm = CPUQVM()
        try:
            qvm.init_qvm()
        except Exception:
            pass

        if hasattr(qvm, "qAlloc_many"):
            qubits = qvm.qAlloc_many(n + 1)
        elif hasattr(qvm, "qalloc_many"):
            qubits = qvm.qalloc_many(n + 1)
        else:
            qubits = [qvm.qAlloc() for _ in range(n + 1)]

        qc = QCircuit()
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                _append(qc, CNOT(qubits[index], qubits[n]))

        try:
            bv_function._machines.append(qvm)
        except AttributeError:
            bv_function._machines = [qvm]

        return qc
