# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, QProg, H, CNOT, measure


def create_ghz(drawing=False):
    qc = QCircuit()
    qc << H(0)
    qc << CNOT(0, 1)
    qc << CNOT(0, 2)

    ghz = QProg()
    ghz << qc
    ghz << measure(0, 0)
    ghz << measure(1, 1)
    ghz << measure(2, 2)

    if drawing:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        return ghz, fig
    return ghz
