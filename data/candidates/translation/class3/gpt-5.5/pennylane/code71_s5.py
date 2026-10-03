# EVAL_META: task_id=71, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit_based_h0_csx01_h1():
    with qml.tape.QuantumTape() as tape:
        qml.Hadamard(wires=0)
        qml.CSX(wires=[0, 1])
        qml.Hadamard(wires=1)
    return tape
