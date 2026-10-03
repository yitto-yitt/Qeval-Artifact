# EVAL_META: task_id=7, framework=pennylane, class=3
import pennylane as qml

def create_parametrized_gate():
    theta = "theta"
    with qml.tape.QuantumTape() as quantum_circuit:
        qml.RX(theta, wires=0)
    return quantum_circuit
