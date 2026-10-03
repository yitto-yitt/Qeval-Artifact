# EVAL_META: task_id=56, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, X

def not_gate(a):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    a = format(a, "08b")
    prog = QCircuit()
    for i in range(8):
        if a[7 - i] == "0":
            prog << X(qubits[i])
    from pyqpanda import QProg, measure_all
    qprog = QProg()
    qprog << prog << measure_all(qubits, cbits)
    shots = 1024
    counts = qvm.run_with_configuration(qprog, cbits, shots)
    total = builtins.sum(counts.values())
    qvm.finalize()
    return {key: value / total for key, value in counts.items()}
