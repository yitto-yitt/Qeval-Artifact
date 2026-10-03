# EVAL_META: task_id=105, framework=cirq, class=3
import cirq


def initialize_cnot_dihedral():
    elem = cirq.CnotDihedral(2)
    elem.cx(0, 1)
    elem.t(0)
    return elem
