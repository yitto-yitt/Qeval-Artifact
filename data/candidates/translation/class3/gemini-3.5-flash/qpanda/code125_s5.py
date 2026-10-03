# EVAL_META: task_id=125, framework=qpanda, class=3
import pyqpanda3.core as pq


def circ_to_gate(circ):
    """
    In pyQPanda, a QCircuit acts as the equivalent of a composite gate (supporting
    methods like .dagger() and .control()). Thus, the circuit itself is returned.
    """
    return circ
