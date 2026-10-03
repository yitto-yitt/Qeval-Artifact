# EVAL_META: task_id=41, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)


def compose_op():
    # Qiskit Pauli("YX") has X on qubit 0, Y on qubit 1.
    # Composing on qargs=[0, 2] maps:
    # qubit 0 of Pauli("YX") (X) -> qubit 0 of the system
    # qubit 1 of Pauli("YX") (Y) -> qubit 2 of the system
    # This results in Y on qubit 2 and X on qubit 0.
    op = pq.PauliOperator({"Y2 X0": 1.0})
    return op


machine.finalize()
