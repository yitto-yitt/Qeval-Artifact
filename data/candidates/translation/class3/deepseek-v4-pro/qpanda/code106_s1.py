# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, T, CNOT

def compose_cnot_dihedral():
    # Build the first circuit: CX(0,1), T(0)
    circ1 = QCircuit()
    circ1 << CNOT(0, 1) << T(0)

    # Build the second circuit: CX(0,1), T(0), X(1)
    circ2 = QCircuit()
    circ2 << CNOT(0, 1) << T(0) << X(1)

    # Composition in CNOT-dihedral order: circ2 first, then circ1
    composed = QCircuit()
    composed << circ2 << circ1
    return composed
