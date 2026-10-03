# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    if isinstance(circuit, qml.tape.QuantumScript):
        tape = circuit
    else:
        func = getattr(circuit, "func", circuit)
        with qml.tape.QuantumTape() as tape:
            func()
            
    wires = list(tape.wires)
    if all(isinstance(w, int) for w in wires):
        wires = sorted(wires)
    if len(wires) == 0:
        wires = [0]
        
    dev = qml.device("default.qubit", wires=wires)
    
    @qml.qnode(dev)
    def state_circuit():
        for op in tape.operations:
            qml.apply(op)
        return qml.state()
        
    return state_circuit()
