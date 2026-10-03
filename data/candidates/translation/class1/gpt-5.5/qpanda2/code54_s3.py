# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def and_gate(a, b):
    machine = init_quantum_machine(QMachineType.CPU)
    try:
        qr_a = machine.qAlloc_many(3)
        qr_b = machine.qAlloc_many(3)
        ancillary = machine.qAlloc_many(3)
        measure = machine.cAlloc_many(3)

        prog = QProg()

        a = format(a, '03b')
        b = format(b, '03b')

        for i in range(3):
            if a[2 - i] == '1':
                prog << X(qr_a[i])
            if b[2 - i] == '1':
                prog << X(qr_b[i])

        for i in range(3):
            prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

        for i in range(3):
            prog << Measure(ancillary[2 - i], measure[i])

        shots = 1024
        counts = machine.run_with_configuration(prog, measure, shots)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        destroy_quantum_machine(machine)
