# EVAL_META: task_id=73, framework=qpanda, class=3
from pyqpanda3.core import CBit, Qubit, H, Measure

def x_measurement(circuit, qubit, clbit):
    if isinstance(qubit, int):
        qubit = Qubit(qubit)
    if isinstance(clbit, int):
        clbit = CBit(clbit)
    circuit << H(qubit)
    circuit << Measure(qubit, clbit)
