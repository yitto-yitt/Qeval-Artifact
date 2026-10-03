# EVAL_META: task_id=3, framework=pennylane, class=2
import pennylane as qml

def create_ghz(drawing=False):
    with qml.tape.QuantumTape() as ghz:
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[0, 2])
        qml.sample(wires=[0, 1, 2])
        
    if drawing:
        dev = qml.device("default.qubit", wires=3)
        
        @qml.qnode(dev)
        def circuit():
            qml.Hadamard(wires=0)
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[0, 2])
            return qml.sample(wires=[0, 1, 2])
            
        fig, ax = qml.draw_mpl(circuit)()
        return ghz, fig
        
    return ghz
