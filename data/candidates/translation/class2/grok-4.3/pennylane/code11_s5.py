# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    sv = circuit()
    return sv
