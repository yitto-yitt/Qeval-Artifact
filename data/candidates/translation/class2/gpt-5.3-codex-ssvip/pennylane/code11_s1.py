# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def get_statevector(circuit):
    num_wires = circuit.num_qubits
    dev = qml.device("default.qubit", wires=num_wires)

    @qml.qnode(dev)
    def qnode():
        qml.from_qiskit(circuit)()
        return qml.state()

    return qnode()
