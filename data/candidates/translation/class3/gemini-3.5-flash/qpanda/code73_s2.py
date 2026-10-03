# EVAL_META: task_id=73, framework=qpanda, class=3
from pyqpanda3.core import H, Measure

def x_measurement(circuit, qubit, clbit):
    circuit << H(qubit) << Measure(qubit, clbit)
    return circuit
