# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, X, Toffoli, BackendType


def and_gate(a, b):
    qvm = QMachine(BackendType.CPU)
    qvm.init()
    try:
        q = qvm.qAlloc_many(9)

        a_bin = format(a, '03b')
        b_bin = format(b, '03b')

        prog = QProg()

        for i in range(3):
            if a_bin[2 - i] == '1':
                prog << X(q[i])

        for i in range(3):
            if b_bin[2 - i] == '1':
                prog << X(q[3 + i])

        for i in range(3):
            prog << Toffoli(q[i], q[3 + i], q[6 + i])

        # Measure in order ancilla[2], ancilla[1], ancilla[0] to match Qiskit output order.
        result = qvm.probRunDict(prog, [q[8], q[7], q[6]])

        return {k: v for k, v in result.items() if v > 1e-12}
    finally:
        qvm.finalize()
