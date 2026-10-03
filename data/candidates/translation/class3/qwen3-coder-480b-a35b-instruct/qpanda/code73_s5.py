# EVAL_META: task_id=73, framework=qpanda, class=3
from pyqpanda3 import *

def x_measurement(circuit, qubit, clbit):
    circuit << H(qubit)
    circuit << Measure(qubit, clbit)
