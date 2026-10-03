# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == 'full':
        num_wires = 2 * num_state_qubits + 2
    elif kind == 'half':
        num_wires = 2 * num_state_qubits + 1
    elif kind == 'fixed':
        num_wires = 2 * num_state_qubits
    else:
        raise ValueError(f"Unsupported kind: {kind}")
    wires = list(range(num_wires))
    with QuantumTape() as tape:
        qml.RippleCarryAdder(wires, num_state_qubits=num_state_qubits, kind=kind)
    return tape
