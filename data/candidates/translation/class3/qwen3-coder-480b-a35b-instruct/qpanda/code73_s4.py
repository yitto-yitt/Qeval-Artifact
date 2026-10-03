# EVAL_META: task_id=73, framework=qpanda, class=3
import pyqpanda3 as pq

def x_measurement(circuit, qubit, clbit):
    circuit << pq.H(qubit)
    circuit << pq.Measure(qubit, clbit)
