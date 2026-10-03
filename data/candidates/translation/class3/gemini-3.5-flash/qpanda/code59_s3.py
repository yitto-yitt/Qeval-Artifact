# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import *

_global_machine = None

def create_cz_gate():
    global _global_machine
    if _global_machine is None:
        _global_machine = CPUQVM()
        _global_machine.init_qvm()
    
    q = _global_machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit << H(q[1]) << CNOT(q[0], q[1]) << H(q[1])
    return circuit
