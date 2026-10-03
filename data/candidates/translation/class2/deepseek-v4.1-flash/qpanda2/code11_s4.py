# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import *

def get_statevector(circuit):
    if isinstance(circuit, QCircuit):
        prog = QProg()
        prog << circuit
    else:
        prog = circuit

    used_qubits = prog.get_used_qubits()
    if not used_qubits:
        return [1 + 0j]
    num_qubits = max([q.get_address() for q in used_qubits]) + 1

    qvm = CPUQVM()
    qvm.init_qvm()
    qvm.qAlloc_many(num_qubits)

    qvm.directly_run(prog)
    state = qvm.get_qstate()
    qvm.finalize()
    return state
