# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *
import numbers

qvm = CPUQVM()
qvm.initQVM()
_qubits = qvm.qAlloc_many(1)

def _has_unassigned_parameters(gate):
    try:
        params = gate.getParameters()
        return any(not isinstance(p, numbers.Real) for p in params)
    except Exception:
        pass

    index = 0
    while index < 1024:
        try:
            param = gate.getParameter(index)
        except Exception:
            break
        if not isinstance(param, numbers.Real):
            return True
        index += 1
    return False

def remove_unassigned_parameterized_gates(circuit):
    filtered = QCircuit()
    for i in range(circuit.getQGateNum()):
        gate = circuit.getQGate(i)
        if not _has_unassigned_parameters(gate):
            filtered << gate
    return filtered

qvm.finalize()
