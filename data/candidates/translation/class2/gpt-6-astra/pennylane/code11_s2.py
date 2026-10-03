# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    device = qml.device("default.qubit", wires=circuit.wires, shots=None)
    tape = qml.tape.QuantumScript(
        operations=circuit.operations,
        measurements=[qml.state()],
        shots=None,
    )
    return qml.execute((tape,), device, diff_method=None)[0]
