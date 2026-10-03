# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(10)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qs = qubits[:n]
    prog = QProg()
    active = []
    for i in range(n):
        p = pauli_string[i].upper()
        if p == 'X':
            prog.insert(H(qs[i]))
            active.append(i)
        elif p == 'Y':
            prog.insert(H(qs[i]))
            prog.insert(Sdag(qs[i]))
            active.append(i)
        elif p == 'Z':
            active.append(i)
    if len(active) == 0:
        return prog
    last = active[-1]
    for i in active[:-1]:
        prog.insert(CNOT(qs[i], qs[last]))
    prog.insert(RZ(qs[last], 2 * time))
    for i in reversed(active[:-1]):
        prog.insert(CNOT(qs[i], qs[last]))
    for i in range(n):
        p = pauli_string[i].upper()
        if p == 'X':
            prog.insert(H(qs[i]))
        elif p == 'Y':
            prog.insert(S(qs[i]))
            prog.insert(H(qs[i]))
    return prog

machine.finalize()
