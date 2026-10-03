# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    if isinstance(circ, qml.tape.QuantumScript):
        if len(circ.operations) == 1:
            return circ.operations[0]
        return qml.prod(*circ.operations)
    elif callable(circ):
        return qml.transforms.make_operator(circ)
    return circ
