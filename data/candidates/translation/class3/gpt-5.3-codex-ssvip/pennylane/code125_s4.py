# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    return qml.ops.functions.bind_new_parameters(circ, ())
