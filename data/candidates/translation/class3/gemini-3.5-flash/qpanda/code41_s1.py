# EVAL_META: task_id=41, framework=qpanda, class=3
from pyqpanda3.core import PauliOperator


def compose_op():
    # Qiskit's Pauli("YX") on qargs=[0, 2] maps:
    # - qubit 0 of YX (which is X) to qubit 0
    # - qubit 1 of YX (which is Y) to qubit 2
    # This corresponds to the Pauli operator Y2 X0.
    return PauliOperator({"Y2 X0": 1.0})
