# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def dj_algorithm(oracle):
    if isinstance(oracle, qml.operation.Operator):
        wires = sorted(list(oracle.wires))
    else:
        with qml.tape.QuantumTape() as tape:
            oracle()
        wires = sorted(list(tape.wires))
    
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
        for w in wires:
            qml.Hadamard(wires=w)
        return qml.probs(wires=wires[:-1])
    
    probs = circuit()
    num_input_qubits = n - 1
    bitstrings = [format(i, f'0{num_input_qubits}b') for i in range(2**num_input_qubits)]
    
    # Qiskit uses little-endian for bitstrings, so we reverse the bitstrings.
    return {bitstrings[i][::-1]: float(probs[i]) for i in range(len(probs))}
