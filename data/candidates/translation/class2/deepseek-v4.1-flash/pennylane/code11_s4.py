# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    dev = qml.device('default.qubit', wires=circuit.wires)
    new_tape = qml.tape.QuantumScript(circuit.operations, [qml.state()])
    return dev.execute(new_tape)[0]
