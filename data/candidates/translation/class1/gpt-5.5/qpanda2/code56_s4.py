# EVAL_META: task_id=56, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, X, Measure

def not_gate(a):
    qvm = CPUQVM()
    qvm.init_qvm()
    shots = 1024
    try:
        qubits = qvm.qAlloc_many(8)
        cbits = qvm.cAlloc_many(8)
        prog = QProg()

        a = format(a, "08b")
        for i in range(8):
            if a[7 - i] == "0":
                prog.insert(X(qubits[i]))

        for i in range(8):
            prog.insert(Measure(qubits[7 - i], cbits[i]))

        counts = qvm.run_with_configuration(prog, cbits, shots)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        qvm.finalize()
