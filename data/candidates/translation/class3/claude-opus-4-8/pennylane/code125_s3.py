# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape


def circ_to_gate(circ):
    if isinstance(circ, QuantumTape):
        tape = circ
    else:
        with QuantumTape() as tape:
            circ()

    wires = tape.wires
    matrix = qml.matrix(tape, wire_order=wires)
    circ_gate = qml.QubitUnitary(matrix, wires=wires)
    return circ_gate
