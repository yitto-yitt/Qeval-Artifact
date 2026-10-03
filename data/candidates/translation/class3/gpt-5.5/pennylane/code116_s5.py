# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    wires = list(range(n_qubits))

    if all(p == "I" for p in pauli_string):
        return qml.tape.QuantumScript([qml.GlobalPhase(time, wires=wires)])

    return qml.tape.QuantumScript([qml.PauliRot(2 * time, pauli_string, wires=wires)])
