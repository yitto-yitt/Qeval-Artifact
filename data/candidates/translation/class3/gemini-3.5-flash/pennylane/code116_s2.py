# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml

def synthesize_evolution_gate(pauli_string, time):
    wires = list(range(len(pauli_string)))
    active_wires = [i for i, char in enumerate(pauli_string) if char != 'I']
    if not active_wires:
        qml.GlobalPhase(-time)
    else:
        qml.PauliRot(2 * time, pauli_string, wires=wires)
