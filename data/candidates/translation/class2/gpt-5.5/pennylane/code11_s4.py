# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
import numpy as np

def get_statevector(circuit):
    tape = None
    wires = None

    if isinstance(circuit, qml.QNode):
        tape = circuit.construct((), {})
        if tape is None:
            tape = getattr(circuit, "_tape", None)
        wires = list(circuit.device.wires)
    elif hasattr(circuit, "operations"):
        tape = circuit
        wires = list(getattr(circuit, "wires", []))
    elif callable(circuit):
        with qml.tape.QuantumTape() as tape:
            circuit()
        wires = list(tape.wires)

    if tape is None:
        raise TypeError("Unsupported circuit type")

    if wires is None or len(wires) == 0:
        wires = list(getattr(tape, "wires", []))

    if len(wires) == 0:
        return np.array([1.0 + 0.0j])

    state_tape = qml.tape.QuantumScript(list(tape.operations), [qml.state()], shots=None)
    dev = qml.device("default.qubit", wires=wires)
    return qml.execute([state_tape], dev)[0]
