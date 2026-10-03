# EVAL_META: task_id=27, framework=pennylane, class=3
import pennylane as qml


def apply_op_back():
    dev = qml.device('default.qubit', wires=3)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.Hadamard(wires=0)
        return qml.state()
    
    # Execute the circuit to build the tape
    circuit()
    tape = circuit.qtape
    
    return tape
