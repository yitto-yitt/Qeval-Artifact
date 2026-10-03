# EVAL_META: task_id=139, framework=pennylane, class=2
import pennylane as qml

def schmidt_test(data, qargs_B):
    return qml.math.schmidt_decomposition(data, qargs_B)
