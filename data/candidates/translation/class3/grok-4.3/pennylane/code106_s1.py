# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml

def compose_cnot_dihedral():
    op_cx = qml.CNOT(wires=[0, 1])
    op_t = qml.T(wires=0)
    elem1 = op_t @ op_cx
    op_x = qml.X(wires=1)
    elem2 = op_x @ op_t @ op_cx
    composed_elem = elem1 @ elem2
    return composed_elem
