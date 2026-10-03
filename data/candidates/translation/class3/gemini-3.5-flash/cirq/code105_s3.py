# EVAL_META: task_id=105, framework=cirq, class=3
import cirq


def initialize_cnot_dihedral():
    elem = cirq.CnotDihedral(2)
    elem.apply_cx(0, 1)
    elem.apply_phase(1, 0)
    return elem
