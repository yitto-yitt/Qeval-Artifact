# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    # Determine the wires
    if hasattr(oracle, "wires") and oracle.wires:
        wires = list(oracle.wires)
    elif hasattr(oracle, "num_qubits"):
        wires = list(range(oracle.num_qubits))
    else:
        try:
            tape = qml.tape.make_tape(oracle)()
            wires = list(tape.wires)
        except Exception:
            wires = []
            
    if not wires:
        if hasattr(oracle, "device") and oracle.device:
            wires = list(oracle.device.wires)
            
    wires = sorted(wires)
    n = len(wires)
    
    dev = qml.device("default.qubit", wires=wires)
    
    @qml.qnode(dev)
    def circuit():
        # State preparation: set output qubit to |1>
        qml.PauliX(wires=wires[-1])
        # Apply Hadamard to all qubits
        for w in wires:
            qml.Hadamard(wires=w)
            
        # Apply oracle
        if hasattr(oracle, "wires"):
            qml.apply(oracle)
        else:
            oracle()
            
        # Apply Hadamard to all qubits
        for w in wires:
            qml.Hadamard(wires=w)
            
        return qml.probs(wires=wires[:-1])
        
    probs = circuit()
    num_input_qubits = n - 1
    bitstrings = [format(i, f"0{num_input_qubits}b") for i in range(2**num_input_qubits)]
    return {bitstring: float(prob) for bitstring, prob in zip(bitstrings, probs)}
