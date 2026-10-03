# EVAL_META: task_id=73, framework=qpanda, class=3
import pyqpanda3.core as pq
def x_measurement(circuit, qubit, clbit):
    circuit << pq.H(qubit) << pq.Measure(qubit, clbit)
