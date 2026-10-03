# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, QProg, H, CNOT, measure


def create_ghz(drawing=False):
    ghz = QProg()
    circuit = QCircuit(3)
    circuit << H(0)
    circuit << CNOT(0, 1)
    circuit << CNOT(0, 2)
    ghz << circuit
    ghz << measure(0, 0)
    ghz << measure(1, 1)
    ghz << measure(2, 2)
    if drawing:
        return ghz, ghz.draw_circuit()
    return ghz
