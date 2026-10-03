# EVAL_META: task_id=55, framework=qpanda2, class=1
from pyqpanda import init_quantum_machine, QMachineType, qAlloc_many, cAlloc_many, QProg, measure, X, Toffoli, run_with_configuration, finalize_quantum_machine
import builtins

def or_gate(a, b):
    machine = init_quantum_machine(QMachineType.CPU)
    qr_a = qAlloc_many(3)
    qr_b = qAlloc_many(3)
    ancillary = qAlloc_many(3)
    measure_c = cAlloc_many(3)

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    prog = QProg()
    for i in range(3):
        if a_bits[2 - i] == '0':
            prog << X(qr_a[i])
        if b_bits[2 - i] == '0':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << X(ancillary[i])

    for i in range(3):
        prog << measure(ancillary[i], measure_c[i])

    shots = 1024
    result = run_with_configuration(prog, shots, measure_c)

    total = builtins.sum(result.values())
    res = {}
    for key, val in result.items():
        if isinstance(key, int):
            bit_str = format(key, '03b')
        else:
            bit_str = key
        res[bit_str] = val / total

    finalize_quantum_machine()
    return res
