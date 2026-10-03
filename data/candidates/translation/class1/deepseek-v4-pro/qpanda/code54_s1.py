# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import *

def and_gate(a, b):
    # Initialize virtual machine
    init_qvm()
    qvm = CPUQVM()
    qvm.init()

    # Allocate qubits: a (3), b (3), ancillary (3)
    qa = qvm.qAlloc_many(3)
    qb = qvm.qAlloc_many(3)
    qanc = qvm.qAlloc_many(3)

    # Build program
    prog = QProg()

    # Encode classical integers onto qubits (LSB at index 0)
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2 - i] == '1':
            prog << X(qa[i])
        if b_bin[2 - i] == '1':
            prog << X(qb[i])

    # Bitwise AND using Toffoli gates
    for i in range(3):
        prog << Toffoli(qa[i], qb[i], qanc[i])

    # Run and obtain probabilities on ancillary qubits
    prob_dist = qvm.prob_run_dict(prog, qanc)

    # Return directly (keys are 3-bit strings, values are probabilities)
    return prob_dist
