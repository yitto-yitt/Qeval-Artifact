# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    if hasattr(circuit, 'wires'):
        wires = circuit.wires
    else:
        wires = qml.wires.Wires([w for op in circuit for w in op.wires])
        
    num_qubits = len(wires)
    
    if isinstance(circuit, qml.tape.QuantumTape):
        mat_target = qml.matrix(circuit, wire_order=wires)
    else:
        tape = qml.tape.QuantumTape(circuit, [])
        mat_target = qml.matrix(tape, wire_order=wires)
        
    qc_list = []
    counter = 0
    
    single_qubit_gates = [qml.H, qml.S, qml.PauliX, qml.PauliY, qml.PauliZ]
    
    while counter < n:
        ops = []
        num_gates = np.random.randint(1, 5 * num_qubits + 1)
        for _ in range(num_gates):
            if num_qubits > 1 and np.random.rand() < 0.3:
                q1, q2 = np.random.choice(num_qubits, 2, replace=False)
                ops.append(qml.CNOT(wires=[wires[q1], wires[q2]]))
            else:
                q = np.random.choice(num_qubits)
                gate = np.random.choice(single_qubit_gates)
                ops.append(gate(wires=wires[q]))
                
        tape = qml.tape.QuantumTape(ops, [])
        mat_qc = qml.matrix(tape, wire_order=wires)
        
        phase = 1.0
        found = False
        for i in range(mat_target.shape[0]):
            for j in range(mat_target.shape[1]):
                if np.abs(mat_target[i, j]) > 1e-8:
                    phase = mat_qc[i, j] / mat_target[i, j]
                    found = True
                    break
            if found:
                break
                
        mat_aligned = mat_target * phase
        
        if np.allclose(mat_qc, mat_aligned, atol=0.4, rtol=0.4):
            qc_list.append(tape)
            counter += 1
            
    return qc_list
