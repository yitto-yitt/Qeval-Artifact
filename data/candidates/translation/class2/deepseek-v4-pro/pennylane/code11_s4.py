# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    if isinstance(circuit, qml.QNode):
        return circuit()
    return qml.devices.qubit.state(circuit)
