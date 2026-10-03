# EVAL_META: task_id=105, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def initialize_cnot_dihedral():
    prog = QProg()
    prog << CNOT(qubits[0], qubits[1])
    prog << T(qubits[0])
    machine.directly_run(prog)
    result = machine.get_qstate()
    return result


if __name__ == "__main__":
    print(initialize_cnot_dihedral())
    machine.finalize()
