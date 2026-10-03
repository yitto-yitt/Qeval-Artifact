# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml


def circ_to_gate(circ):
    def gate(*args, **kwargs):
        if callable(circ):
            return circ(*args, **kwargs)
        for op in circ:
            qml.apply(op)

    return gate
