# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    wires = circuit.wires
    dev = qml.device('default.qubit', wires=wires)
    tape = qml.tape.QuantumScript(circuit.operations, [qml.state()])
    result = qml.execute([tape], dev, gradient_fn=None)[0]
    return result
