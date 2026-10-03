# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, CPUQVM, X, T, CNOT
import numpy as np


def _circ_unitary(builder, n):
    qvm = CPUQVM()
    dim = 1 << n
    cols = []
    for basis in range(dim):
        prog = QProg()
        for q in range(n):
            if (basis >> q) & 1:
                prog << X(q)
        c = QCircuit()
        builder(c)
        prog << c
        qvm.run(prog, 0)
        sv = np.array(qvm.result().get_state_vector())
        cols.append(sv)
    U = np.column_stack(cols)
    return U


def compose_cnot_dihedral():
    n = 2

    def build1(c):
        c << CNOT(0, 1)
        c << T(0)

    def build2(c):
        build1(c)
        c << X(1)

    U1 = _circ_unitary(build1, n)
    U2 = _circ_unitary(build2, n)

    # compose: elem1.compose(elem2) applies elem1 then elem2 => U2 @ U1
    composed = U2 @ U1
    return composed
