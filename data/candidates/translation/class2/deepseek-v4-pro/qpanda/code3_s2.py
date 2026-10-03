# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit


def create_ghz(drawing=False):
    ghz = QuantumCircuit(3)
    ghz.h(0)
    ghz.cnot(0, 1)
    ghz.cnot(0, 2)
    ghz.measure_all()
    if drawing:
        return ghz, ghz.draw(output="mpl")
    return ghz
