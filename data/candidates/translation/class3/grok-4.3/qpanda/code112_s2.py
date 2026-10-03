# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, create_empty_qprog, H, RZ, RX, CNOT
import math

def create_product_formula_circuit(pauli_strings, times, order, reps):
    if len(pauli_strings) == 0:
        qvm = CPUQVM()
        qvm.init_qvm()
        return create_empty_qprog()
    num_qubits = len(pauli_strings[0])
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    prog = create_empty_qprog()
    def add_pauli_rotation(prg, qs, pauli, phi):
        non_i = [(i, p) for i, p in enumerate(pauli) if p != 'I']
        if len(non_i) == 0:
            return
        for idx, p in non_i:
            if p == 'X':
                prg << H(qs[idx])
            elif p == 'Y':
                prg << RZ(qs[idx], -math.pi / 2)
                prg << H(qs[idx])
        for k in range(len(non_i) - 1):
            ctrl = non_i[k][0]
            tgt = non_i[k + 1][0]
            prg << CNOT(qs[ctrl], qs[tgt])
        last = non_i[-1][0]
        prg << RZ(qs[last], phi)
        for k in reversed(range(len(non_i) - 1)):
            ctrl = non_i[k][0]
            tgt = non_i[k + 1][0]
            prg << CNOT(qs[ctrl], qs[tgt])
        for idx, p in reversed(non_i):
            if p == 'X':
                prg << H(qs[idx])
            elif p == 'Y':
                prg << H(qs[idx])
                prg << RZ(qs[idx], math.pi / 2)
    for pauli_str, t in zip(pauli_strings, times):
        dt = t / reps if reps > 0 else 0.0
        for _ in range(reps):
            add_pauli_rotation(prog, qubits, pauli_str, 2.0 * dt)
    return prog
