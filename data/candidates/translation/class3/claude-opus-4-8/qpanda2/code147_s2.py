# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def mcy(qc):
    controls = [qubits[0], qubits[1], qubits[2], qubits[3]]
    target = qubits[4]
    qc << RZ(target, -3.141592653589793 / 2)
    qc << Y(target).control(controls)
    qc << RZ(target, 3.141592653589793 / 2)
    return qc


if __name__ == "__main__":
    prog = QProg()
    prog << H(qubits[0]) << H(qubits[1]) << H(qubits[2]) << H(qubits[3])
    mcy(prog)
    machine.directly_run(prog)
    result = machine.get_qstate()
    print(result)
    machine.finalize()
