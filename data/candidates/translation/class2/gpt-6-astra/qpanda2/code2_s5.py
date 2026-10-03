# EVAL_META: task_id=2, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg, H, CNOT


def create_bell_statevector():
    machine = CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(2)
        program = QProg()
        program << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        machine.directly_run(program)
        return machine.get_qstate()
    finally:
        machine.finalize()
