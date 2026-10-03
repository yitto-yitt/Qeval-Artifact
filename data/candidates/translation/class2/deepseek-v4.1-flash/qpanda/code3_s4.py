# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QProg, H, CNOT, Measure

def create_ghz(drawing=False):
    ghz = QProg()
    ghz << H(0) << CNOT(0, 1) << CNOT(0, 2)
    ghz << Measure(0, 0) << Measure(1, 1) << Measure(2, 2)
    if drawing:
        return ghz, ghz.draw()
    return ghz
