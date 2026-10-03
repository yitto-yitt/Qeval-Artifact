# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    wires = list(circuit.wires) if hasattr(circuit, 'wires') else [0]
    if not wires:
        wires = [0]
    w0 = wires[0]
    
    ops = list(circuit.operations) if hasattr(circuit, 'operations') else []
    meas = list(circuit.measurements) if hasattr(circuit, 'measurements') else []
    
    qc_list = []
    for i in range(n):
        extra_ops = []
        num_pairs = np.random.randint(1, 5)
        for _ in range(num_pairs):
            gate = np.random.randint(0, 4)
            if gate == 0:
                extra_ops.extend([qml.Hadamard(w0), qml.Hadamard(w0)])
            elif gate == 1:
                extra_ops.extend([qml.PauliX(w0), qml.PauliX(w0)])
            elif gate == 2:
                extra_ops.extend([qml.PauliZ(w0), qml.PauliZ(w0)])
            else:
                extra_ops.extend([qml.S(w0), qml.S(w0), qml.S(w0), qml.S(w0)])
                
        new_ops = extra_ops + ops
        new_tape = qml.tape.QuantumTape(new_ops, meas)
        qc_list.append(new_tape)
        
    return qc_list
