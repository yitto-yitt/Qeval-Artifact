# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np
from pennylane.templates.subroutines import CDKMRippleCarryAdder

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    adder = CDKMRippleCarryAdder(num_state_qubits, kind)
    num_qubits = 2 * num_state_qubits + 2  # CDKMRippleCarryAdder uses 2*num_state_qubits + 2 qubits
    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        adder()
        return qml.state()

    return circuit
