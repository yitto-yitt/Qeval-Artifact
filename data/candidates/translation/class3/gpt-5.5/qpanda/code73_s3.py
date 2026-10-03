# EVAL_META: task_id=73, framework=qpanda, class=3
import pyqpanda3.core as pq


def x_measurement(circuit, qubit, clbit):
    circuit << pq.H(qubit)
    measure_op = getattr(pq, "Measure", None)
    if measure_op is None:
        measure_op = getattr(pq, "measure")
    circuit << measure_op(qubit, clbit)
