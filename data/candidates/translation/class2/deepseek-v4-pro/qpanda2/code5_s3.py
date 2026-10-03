# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import *

_initialized = False

def create_state_prep():
    global _initialized
    if not _initialized:
        try:
            init(QMachineType.CPU)
        except Exception:
            pass
        _initialized = True
    qubits = qAlloc_many(2)
    qc = QCircuit()
    qc << X(qubits[0])
    return qc
