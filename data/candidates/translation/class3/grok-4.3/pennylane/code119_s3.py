# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml
from pennylane.templates.arithmetic import CDKMRippleCarryAdder
from pennylane.tape import QuantumScript

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == "full":
        n_qubits = 2 * num_state_qubits + 2
    elif kind == "half":
        n_qubits = 2 * num_state_qubits + 1
    else:
        n_qubits = 2 * num_state_qubits
    wires = list(range(n_qubits))
    op = CDKMRippleCarryAdder(num_state_qubits, wires=wires, kind=kind)
    return QuantumScript([op])
