# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, StateVector

def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init_qvm()
    prog = QProg()
    prog << circuit
    qvm.run(prog)
    sv = qvm.get_statevector()
    qvm.finalize()
    return sv
