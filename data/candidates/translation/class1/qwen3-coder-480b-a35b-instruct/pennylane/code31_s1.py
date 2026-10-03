# EVAL_META: task_id=31, framework=pennylane, class=1
import pennylane as qml
from typing import Dict

def sampler_qiskit() -> Dict[str, float]:
    dev = qml.device('default.qubit', wires=2, shots=1000)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])

    probs = bell_circuit()
    basis_states = ['00', '01', '10', '11']
    return dict(zip(basis_states, probs))
