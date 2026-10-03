# EVAL_META: task_id=3, framework=pennylane, class=2
import pennylane as qml
import numpy as np


def create_ghz(drawing=False):
    dev = qml.device('default.qubit', wires=3)
    
    @qml.qnode(dev)
    def ghz_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        return [qml.sample(qml.PauliZ(i)) for i in range(3)]
    
    # Execute the circuit to prepare it
    _ = ghz_circuit()
    
    if drawing:
        drawer = qml.draw(ghz_circuit)
        return ghz_circuit, drawer()
    return ghz_circuit
