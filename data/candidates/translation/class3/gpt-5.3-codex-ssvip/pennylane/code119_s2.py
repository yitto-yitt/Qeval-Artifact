# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    op = qml.CDKMRippleCarryAdder(num_state_qubits, wires=range(2 * num_state_qubits + (2 if kind == "full" else 1)), kind=kind)
    return qml.tape.QuantumTape([op], [])
