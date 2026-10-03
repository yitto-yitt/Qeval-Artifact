# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import *
def xor_gate(a, b):
    qm = QuantumMachine()
    qs = qm.allocate_qubits(8)
    cs = qm.allocate_cbits(8)
    prog = QProg()
    for i in range(8):
        if (a >> i) & 1:
            prog.insert(X(qs[i]))
    for i in range(8):
        if (b >> i) & 1:
            prog.insert(X(qs[i]))
    prog.insert(Measure(qs, cs))
    res = qm.run(prog, shots=1024)
    counts = res.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
