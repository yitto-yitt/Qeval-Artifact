# EVAL_META: task_id=73, framework=qpanda, class=3
from pyqpanda import *

def x_measurement(circuit, qubit, clbit):
    circuit.insert(H(qubit))
    circuit.insert(MEASURE(qubit, clbit))
