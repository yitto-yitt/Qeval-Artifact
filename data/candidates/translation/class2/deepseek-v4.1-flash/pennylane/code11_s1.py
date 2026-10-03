# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    dev = qml.device("default.qubit", wires=circuit.device.wires)
    @qml.qnode(dev)
    def state_circuit():
        circuit.func()
        return qml.state()
    return state_circuit()
