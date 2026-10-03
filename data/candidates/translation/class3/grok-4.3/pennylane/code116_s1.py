# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml

def synthesize_evolution_gate(pauli_string, time):
    n_wires = len(pauli_string)
    op = qml.PauliRot(2 * time, pauli_string, wires=range(n_wires))
    return qml.tape.QuantumScript([op])
