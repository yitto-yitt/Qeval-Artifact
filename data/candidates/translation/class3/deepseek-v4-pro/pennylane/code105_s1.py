# EVAL_META: task_id=105, framework=pennylane, class=3
import pennylane as qml

def initialize_cnot_dihedral():
    ops = [qml.CNOT(wires=[0, 1]), qml.T(wires=0)]
    tape = qml.tape.QuantumScript(ops)
    return tape
