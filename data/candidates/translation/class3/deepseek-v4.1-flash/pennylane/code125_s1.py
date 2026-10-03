# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml

def circ_to_gate(circ):
    if isinstance(circ, qml.tape.QuantumTape):
        tape = circ
    else:
        with qml.tape.QuantumTape() as tape:
            circ()
    matrix = qml.matrix(tape)
    return qml.QubitUnitary(matrix, wires=tape.wires)
