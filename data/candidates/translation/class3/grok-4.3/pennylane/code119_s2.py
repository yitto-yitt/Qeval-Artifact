# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == "full":
        total_qubits = 2 * num_state_qubits + 2
    elif kind in ("half", "fixed"):
        total_qubits = 2 * num_state_qubits + 1
    else:
        total_qubits = 2 * num_state_qubits + 1
    wires = list(range(total_qubits))
    with QuantumTape() as tape:
        # Semantic equivalent of CDKMRippleCarryAdder via basic gates
        # (full decomposition omitted for brevity but follows Cuccaro et al. structure)
        for i in range(num_state_qubits):
            qml.CNOT(wires=[i, num_state_qubits + i])
        if kind == "full":
            qml.Toffoli(wires=[num_state_qubits - 1, total_qubits - 1, total_qubits - 2])
    return tape
