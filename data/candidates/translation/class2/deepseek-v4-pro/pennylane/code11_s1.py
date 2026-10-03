# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    with qml.tape.QuantumTape() as tape:
        circuit()
    wires = tape.wires
    dev = qml.device("default.qubit", wires=wires)
    results = qml.execute([tape], dev, None)
    return results[0]
