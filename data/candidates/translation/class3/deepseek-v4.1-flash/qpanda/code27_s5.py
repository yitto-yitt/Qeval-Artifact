# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, CNOT


def apply_op_back():
    # Build the 3-qubit circuit: H on qubit 0, then CNOT(0 -> 1)
    circuit = QCircuit()
    circuit << H(0)
    circuit << CNOT(0, 1)

    # Analogous to Qiskit's DAGCircuit.apply_operation_back(HGate(), [q[0]]):
    # append a Hadamard operation to the back of qubit 0.
    circuit << H(0)

    # Wrap into a QProg (executable program representation) and return it.
    prog = QProg()
    prog << circuit
    return prog
