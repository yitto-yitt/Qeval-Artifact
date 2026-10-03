# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    tape = qml.tape.QuantumScript(circuit.operations, [qml.state()])
    dev = qml.device("default.qubit", wires=tape.wires)
    return dev.execute(tape)
