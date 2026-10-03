# EVAL_META: task_id=108, framework=qpanda2, class=3
from pyqpanda import CPUQVM, qAlloc_many
from pyqpanda.quantum_info import Choi

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(2)

def initialize_adjoint_and_compose(data1, data2):
    choi1 = Choi(data1)
    choi2 = Choi(data2)
    adjoint_choi1 = choi1.adjoint()
    composed_choi = choi1.compose(choi2)
    return choi1, adjoint_choi1, composed_choi

# Manual cleanup
machine.finalize()
