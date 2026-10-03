# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import *

def get_statevector(circuit):
    qubits = circuit.get_used_qubits()
    if qubits:
        qvm = qubits[0].get_owner()
    else:
        qvm = CPUQVM()
        qvm.init_qvm()
    if isinstance(circuit, QProg):
        prog = circuit
    else:
        prog = QProg()
        prog << circuit
    qvm.directly_run(prog)
    return qvm.get_qstate()
