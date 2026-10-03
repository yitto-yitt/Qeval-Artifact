# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, H, CNOT, measure_all
def bv_algorithm(s):
    n = len(s)
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n + 1)
    cbits = qvm.cAlloc_many(n)
    prog = QProg()
    ancilla = n
    prog << X(qubits[ancilla])
    for i in range(n + 1):
        prog << H(qubits[i])
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(qubits[index], qubits[ancilla])
    for i in range(n):
        prog << H(qubits[i])
    prog << measure_all(qubits[0:n], cbits)
    result = qvm.run_with_configuration(prog, cbits, shots=1)
    bitstrings = list(result.keys())
    return [bitstrings, result]
