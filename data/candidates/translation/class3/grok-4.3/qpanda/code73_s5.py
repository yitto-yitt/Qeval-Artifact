# EVAL_META: task_id=73, framework=qpanda, class=3
from pyqpanda3.core import *
def x_measurement(circuit, qubit, clbit):
    circuit.h(qubit)
    circuit.measure(qubit, clbit)
