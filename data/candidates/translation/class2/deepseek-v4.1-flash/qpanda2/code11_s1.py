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
        return [1.0+0j]
    machine = used_qubits[0].get_machine()
    machine.run(prog)
    return machine.get_qstate()
