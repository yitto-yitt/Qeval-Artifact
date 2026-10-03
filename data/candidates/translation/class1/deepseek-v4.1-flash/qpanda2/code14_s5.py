# EVAL_META: task_id=14, framework=qpanda2, class=1
from pyqpanda import CPUQVM, QProg, H, CNOT, measure
import builtins

def bell_each_shot():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog << measure(qubits[0], cbits[0]) << measure(qubits[1], cbits[1])
    counts = qvm.run_with_configuration(prog, cbits, 10)
    qvm.finalize()
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
