# EVAL_META: task_id=108, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, Circuit

def initialize_adjoint_and_compose(data1, data2):
    machine = QuantumMachine()
    q = machine.alloc_qubits(2)
    c = machine.alloc_cbits(2)
    choi1 = Circuit(machine).insert(data1)
    choi2 = Circuit(machine).insert(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi
