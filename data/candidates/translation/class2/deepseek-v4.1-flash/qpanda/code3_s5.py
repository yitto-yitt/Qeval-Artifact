# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, H, CNOT, measure


def create_ghz(drawing=False):
    ghz = QCircuit(3)
    ghz << H(0)
    ghz << CNOT(0, 1)
    ghz << CNOT(0, 2)
    ghz << measure(0, 0)
    ghz << measure(1, 1)
    ghz << measure(2, 2)
    if drawing:
        return ghz, ghz.draw()
    return ghz
