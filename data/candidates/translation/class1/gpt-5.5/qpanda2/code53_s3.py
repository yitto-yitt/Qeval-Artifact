# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, X, Measure

def xor_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(8)
        cbits = qvm.cAlloc_many(8)

        prog = QProg()

        for value in (int(a), int(b)):
            for i in range(8):
                if (value >> i) & 1:
                    prog << X(qubits[i])

        for i in range(8):
            prog << Measure(qubits[i], cbits[i])

        shots = 1024
        counts = qvm.run_with_configuration(prog, cbits, shots)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        qvm.finalize()
