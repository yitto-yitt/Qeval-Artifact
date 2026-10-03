# EVAL_META: task_id=119, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(30)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == 'full':
        n = num_state_qubits
        total = 2 * n + 2
    elif kind == 'half':
        n = num_state_qubits
        total = 2 * n + 1
    else:
        n = num_state_qubits
        total = 2 * n
    qs = qubits[:total]
    prog = QProg()
    if total < 3:
        return prog
    # CDKM ripple-carry structure (MAJ + UMA cascade)
    # cin at qs[0], a at qs[1:1+n], b at qs[1+n:1+2*n], cout at last
    for i in range(n):
        prog << CNOT(qs[i], qs[n + 1 + i])
        prog << CNOT(qs[n + 1 + i], qs[i + 1])
        prog << Toffoli(qs[i], qs[n + 1 + i], qs[i + 1])
    for i in range(n - 1, -1, -1):
        prog << Toffoli(qs[i], qs[n + 1 + i], qs[i + 1])
        prog << CNOT(qs[n + 1 + i], qs[i + 1])
        prog << CNOT(qs[i + 1], qs[n + 1 + i])
        if i > 0:
            prog << CNOT(qs[i], qs[i - 1])
    return prog

machine.finalize()
