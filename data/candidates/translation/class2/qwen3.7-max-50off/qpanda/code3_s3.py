# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QCircuit

def create_ghz(drawing=False):
    ghz = QCircuit(3)
    ghz.h(0)
    ghz.cx(0, 1)
    ghz.cx(0, 2)
    ghz.measure_all()
    if drawing:
        return ghz, ghz.draw()
    return ghz
