# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml


def create_state_prep(num_qubits):
    with qml.tape.QuantumTape() as tape:
        qml.BasisState([1] + [0] * (num_qubits - 1), wires=range(num_qubits))
    return tape
