# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, QProg, H, CNOT, measure


def create_ghz(drawing=False):
    ghz = QCircuit()
    ghz << H(0)
    ghz << CNOT(0, 1)
    ghz << CNOT(0, 2)

    prog = QProg()
    prog << ghz
    for i in range(3):
        prog << measure(i, i)

    if drawing:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        return prog, fig
    return prog
