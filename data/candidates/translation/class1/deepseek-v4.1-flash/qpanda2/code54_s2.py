# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, X, Toffoli, Measure


def and_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()

    qubits = machine.qAlloc_many(9)
    cbits = machine.cAlloc_many(3)

    prog = QProg()

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    for i in range(3):
        if a_bits[2 - i] == '1':
            prog << X(qubits[i])
        if b_bits[2 - i] == '1':
            prog << X(qubits[3 + i])

    for i in range(3):
        prog << Toffoli(qubits[i], qubits[3 + i], qubits[6 + i])

    for i in range(3):
        prog << Measure(qubits[6 + i], cbits[i])

    shots = 1000
    result = machine.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
