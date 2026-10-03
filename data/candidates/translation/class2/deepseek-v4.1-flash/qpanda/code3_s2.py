# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, QProg, H, CNOT, measure
from pyqpanda3.visualization import draw_qprog

def create_ghz(drawing=False):
    ghz = QCircuit()
    ghz << H(0)
    ghz << CNOT(0, 1)
    ghz << CNOT(0, 2)
    ghz << measure(0, 0)
    ghz << measure(1, 1)
    ghz << measure(2, 2)
    if drawing:
        prog = QProg()
        prog << ghz
        fig = draw_qprog(prog, output='mpl')
        return ghz, fig
    return ghz
