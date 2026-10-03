# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import *
def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    circ = QCircuit()
    for pstr, t in zip(pauli_strings, times):
        dt = t / reps
        for _ in range(reps):
            for i, p in enumerate(pstr):
                if p == 'X':
                    circ << H(q[i])
                elif p == 'Y':
                    circ << RX(q[i], 1.5707963267948966)
            for i, p in enumerate(pstr):
                if p in 'XYZ':
                    circ << RZ(q[i], 2 * dt)
            for i, p in enumerate(reversed(pstr)):
                j = n - 1 - i
                if p == 'X':
                    circ << H(q[j])
                elif p == 'Y':
                    circ << RX(q[j], -1.5707963267948966)
    prog = QProg()
    prog << circ
    return prog
