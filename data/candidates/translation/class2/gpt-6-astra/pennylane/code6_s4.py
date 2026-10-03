# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml


def create_state_prep(num_qubits):
    wires = list(reversed(range(num_qubits)))
    return qml.tape.QuantumScript(
        [qml.BasisState(1, wires=wires)]
    )
