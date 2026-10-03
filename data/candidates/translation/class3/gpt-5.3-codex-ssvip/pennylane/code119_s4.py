# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    adder = qml.CDKMRippleCarryAdder(wires=range(2 * num_state_qubits + (2 if kind == "full" else 1 if kind == "half" else 0) + 1), kind=kind)
    return qml.tape.QuantumScript(ops=[adder], measurements=[])
