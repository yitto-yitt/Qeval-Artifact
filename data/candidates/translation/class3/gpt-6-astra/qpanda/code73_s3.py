# EVAL_META: task_id=73, framework=qpanda, class=3
import pyqpanda3.core as pq


def x_measurement(circuit, qubit, clbit):
    measure = getattr(pq, "measure", None) or getattr(pq, "Measure")
    circuit << pq.H(qubit)
    circuit << measure(qubit, clbit)
