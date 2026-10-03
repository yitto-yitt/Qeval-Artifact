# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
from pennylane.tape import QuantumTape

def get_statevector(circuit):
    if isinstance(circuit, qml.QNode):
        ops = circuit.tape.operations
        dev = circuit.device
    elif isinstance(circuit, QuantumTape):
        ops = circuit.operations
        wires = list(circuit.wires) if circuit.wires else [0]
        dev = qml.device("default.qubit", wires=wires)
    else:
        with QuantumTape() as tape:
            circuit()
        ops = tape.operations
        wires = list(tape.wires) if tape.wires else [0]
        dev = qml.device("default.qubit", wires=wires)

    state_tape = QuantumTape(ops, [qml.state()])
    return qml.execute([state_tape], dev, None)[0]
