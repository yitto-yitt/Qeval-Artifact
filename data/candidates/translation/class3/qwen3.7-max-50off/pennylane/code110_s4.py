# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    if hasattr(circuit, 'operations'):
        ops = circuit.operations
        meas = circuit.measurements
        wires = circuit.wires
    else:
        ops = []
        meas = []
        wires = [0]

    num_qubits = len(wires)
    if num_qubits == 0:
        wires = [0]
        num_qubits = 1

    qc_list = []
    
    for i in range(n):
        w = np.random.choice(wires)
        seq_type = np.random.randint(0, 5)
        if seq_type == 0:
            seq = [qml.H(w), qml.H(w)]
        elif seq_type == 1:
            seq = [qml.X(w), qml.X(w)]
        elif seq_type == 2:
            seq = [qml.Y(w), qml.Y(w)]
        elif seq_type == 3:
            seq = [qml.Z(w), qml.Z(w)]
        else:
            seq = [qml.S(w), qml.S(w), qml.S(w), qml.S(w)]
            
        new_ops = seq + list(ops)
        new_tape = qml.tape.QuantumTape(new_ops, list(meas))
        qc_list.append(new_tape)
        
    return qc_list
