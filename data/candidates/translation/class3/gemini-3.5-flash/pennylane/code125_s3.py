# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml

def circ_to_gate(circ):
    if hasattr(circ, "operations"):
        return qml.prod(*circ.operations)
    elif callable(circ):
        return qml.transforms.make_operator(circ)
    return circ
