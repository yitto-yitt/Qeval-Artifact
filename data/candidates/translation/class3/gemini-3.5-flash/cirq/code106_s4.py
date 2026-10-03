# EVAL_META: task_id=106, framework=cirq, class=3
import cirq


def compose_cnot_dihedral():
    elem = cirq.CnotDihedral(2)
    elem.apply_cx(0, 1)
    elem.apply_phase(1, 0)
    elem.apply_cx(0, 1)
    elem.apply_phase(1, 0)
    elem.apply_x(1)
    return elem
