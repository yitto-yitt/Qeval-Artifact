# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, QProg, H, CNOT, measure


def create_ghz(drawing=False):
    ghz = QProg()
    circuit = QCircuit()
    circuit << H(0)
    circuit << CNOT(0, 1)
    circuit << CNOT(0, 2)
    ghz << circuit
    for i in range(3):
        ghz << measure(i, i)
    if drawing:
        return ghz, ghz.draw_circuit()
    return ghz
