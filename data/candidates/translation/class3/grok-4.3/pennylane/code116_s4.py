# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    wires = range(n_qubits)
    with qml.tape.QuantumTape() as tape:
        qml.PauliRot(2 * time, pauli_string, wires=wires)
    return tape
