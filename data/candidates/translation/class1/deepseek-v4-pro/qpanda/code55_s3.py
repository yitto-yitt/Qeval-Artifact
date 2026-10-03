# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QMachineType, QProg, QuantumCircuit


def or_gate(a, b):
    machine = QMachine(QMachineType.CPU)
    q = machine.qAlloc_many(9)
    c = machine.cAlloc_many(3)

    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    qc = QuantumCircuit(q)

    for i in range(3):
        if a_bin[2 - i] == '0':
            qc.x(q[i])
        if b_bin[2 - i] == '0':
            qc.x(q[3 + i])

    for i in range(3):
        qc.ccx(q[i], q[3 + i], q[6 + i])

    for i in range(3):
        qc.x(q[6 + i])

    for i in range(3):
        qc.measure(q[6 + i], c[i])

    prog = QProg()
    prog << qc

    result = machine.run_with_configuration(prog, c, 1024)
    total = sum(result.values())

    return {key: value / total for key, value in result.items()}
