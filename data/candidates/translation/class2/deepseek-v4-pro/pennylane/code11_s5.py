# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
from pennylane.tape import QuantumScript

def get_statevector(circuit):
    if isinstance(circuit, qml.QNode):
        circuit()
        ops = circuit.tape.operations
        dev = circuit.device
    elif isinstance(circuit, QuantumScript):
        ops = circuit.operations
        dev = qml.device("default.qubit", wires=circuit.wires)
    else:
        return circuit()

    tape = QuantumScript(ops, [qml.state()])
    return qml.execute([tape], dev, gradient_fn=None)[0]
