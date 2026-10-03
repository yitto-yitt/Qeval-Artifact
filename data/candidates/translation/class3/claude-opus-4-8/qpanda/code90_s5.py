# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X, H

def create_custom_controlled():
    qubits = list(range(4))

    # Custom 2-qubit gate: X on qubit 0, H on qubit 1 (of the sub-gate).
    # Controls: physical qubits 0 and 3; Targets: physical qubits 1 and 2.
    controls = [qubits[0], qubits[3]]

    x_gate = X(qubits[1])
    x_gate.control(controls)

    h_gate = H(qubits[2])
    h_gate.control(controls)

    circuit = QCircuit()
    circuit << x_gate
    circuit << h_gate

    prog = QProg()
    prog << circuit
    return prog
