# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import init_quantum_machine, QMachineType, create_empty_qprog, H

def create_uniform_superposition(n):
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(n)
    prog = create_empty_qprog()
    for q in qubits:
        prog << H(q)
    machine.directly_run(prog)
    statevector = machine.get_qstate()
    machine.finalize()
    return statevector
