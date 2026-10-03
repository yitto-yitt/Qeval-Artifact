# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, Measure

def dj_algorithm(oracle):
    n = oracle.qubit_num()
    qvm = CPUQVM()
    qvm.init_qvm(n)
    qubits = qvm.qAlloc_many(n)
    cbits = qvm.cAlloc_many(n - 1)
    prog = QProg()
    prog << X(qubits[n - 1])
    for i in range(n):
        prog << H(qubits[i])
    prog << oracle
    for i in range(n):
        prog << H(qubits[i])
    for i in range(n - 1):
        prog << Measure(qubits[n - 2 - i], cbits[i])
    result = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
