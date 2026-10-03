# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, QCircuit

def get_statevector(circuit):
    if isinstance(circuit, QCircuit):
        prog = QProg()
        prog << circuit
    else:
        prog = circuit
    qvm = CPUQVM()
    qvm.run(prog)
    return qvm.get_qstate()
