# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, QProg, H, X

def dj_algorithm(oracle):
    n = oracle["num_qubits"]
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    cbits = qvm.cAlloc_many(n - 1)

    prog = QProg()
    prog << X(qubits[n - 1])
    for i in range(n):
        prog << H(qubits[i])
    prog << oracle["build"](qubits)
    for i in range(n):
        prog << H(qubits[i])
    for i in range(n - 1):
        prog << oracle
    # measure input register
    from pyqpanda import Measure
    for i in range(n - 1):
        prog << Measure(qubits[i], cbits[i])

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    result = {}
    for key, value in counts.items():
        result[key] = value / total
    qvm.finalize()
    return result
