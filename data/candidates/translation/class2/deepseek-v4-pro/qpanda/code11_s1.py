# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import *

def get_statevector(circuit):
    if not is_initialized():
        init_quantum_machine(QMachineType.CPU)
    qvm = QVM()
    state = qvm.getStateVector(circuit)
    return state
