# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def dj_algorithm(oracle):
    qubits = oracle.get_qubits()
    qubits = sorted(qubits, key=lambda q: q.get_addr())
    n = len(qubits)
    output_qubit = qubits[-1]
    input_qubits = qubits[:-1]
    
    qvm = CPUQVM()
    qvm.init_qvm()
    cbits = qvm.cAlloc_many(n - 1)
    
    prog = QProg()
    prog << X(output_qubit)
    for q in qubits:
        prog << H(q)
    prog << oracle
    for q in qubits:
        prog << H(q)
    for i, q in enumerate(input_qubits):
        prog << Measure(q, cbits[i])
    
    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    probs = {key[::-1]: count / total for key, count in counts.items()}
    return probs
