# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import QuantumCircuit


def create_ghz(drawing=False):
    ghz = QuantumCircuit(3)
    ghz.h(0)
    ghz.cx(0, 1)
    ghz.cx(0, 2)
    ghz.measure_all()
    if drawing:
        return ghz, ghz.draw(output="mpl")
    return ghz
