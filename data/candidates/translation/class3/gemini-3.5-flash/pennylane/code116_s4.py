# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml

def synthesize_evolution_gate(pauli_string, time):
    def circuit():
        active_paulis = []
        active_wires = []
        for i, char in enumerate(pauli_string):
            if char != 'I':
                active_paulis.append(char)
                active_wires.append(i)
        
        if not active_paulis:
            qml.GlobalPhase(-time, wires=list(range(len(pauli_string))))
        else:
            qml.PauliRot(2 * time, "".join(active_paulis), wires=active_wires)
            
    return circuit
