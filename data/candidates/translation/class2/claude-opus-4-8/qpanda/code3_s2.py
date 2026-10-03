# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QProg, QCircuit, H, CNOT, measure


def create_ghz(drawing=False):
    ghz = QProg()
    circ = QCircuit(3)
    circ << H(0)
    circ << CNOT(0, 1)
    circ << CNOT(0, 2)
    ghz << circ
    for i in range(3):
        ghz << measure(i, i)
    if drawing:
        return ghz, ghz.draw_circuit() if hasattr(ghz, "draw_circuit") else str(ghz)
    return ghz
