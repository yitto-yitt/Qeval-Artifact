# EVAL_META: task_id=61, framework=pennylane, class=1
import pennylane as qml

def create_quantum_circuit_with_one_qubit_and_measure():
    with qml.tape.QuantumTape() as tape:
        qml.sample(wires=0)
    return tape
