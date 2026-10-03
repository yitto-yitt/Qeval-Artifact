# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    if hasattr(oracle, "wires") and oracle.wires:
        wires = list(oracle.wires)
    else:
        tape = qml.tape.make_tape(oracle)()
        wires = list(tape.wires)
        
    wires = sorted(wires)
    n = len(wires)
    
    dev = qml.device("default.qubit", wires=wires)
    
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=wires[-1])
        for w in wires:
            qml.Hadamard(wires=w)
        
        if isinstance(oracle, qml.operation.Operator):
            qml.apply(oracle)
        else:
            oracle()
            
        for w in wires[:-1]:
            qml.Hadamard(wires=w)
            
        return qml.probs(wires=wires[:-1])
        
    probs = circuit()
    probs = qml.math.toarray(probs)
    
    num_input_qubits = n - 1
    bitstrings = [format(i, f'0{num_input_qubits}b') for i in range(2**num_input_qubits)]
    
    return {bitstrings[i]: float(probs[i]) for i in range(len(probs))}
