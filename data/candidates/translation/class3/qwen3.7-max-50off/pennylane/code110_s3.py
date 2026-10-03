# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    try:
        U_orig = qml.matrix(circuit)
        if callable(U_orig):
            U_orig = U_orig()
    except Exception:
        U_orig = qml.matrix(circuit)()
        
    num_qubits = int(np.round(np.log2(U_orig.shape[0])))
    
    qc_list = []
    counter = 0
    
    while counter < n:
        ops = []
        depth = np.random.randint(num_qubits, 4 * num_qubits + 2)
        for _ in range(depth):
            gate = np.random.choice(['H', 'S', 'X', 'Z', 'CNOT'])
            if gate == 'CNOT' and num_qubits > 1:
                q1, q2 = np.random.choice(num_qubits, 2, replace=False)
                ops.append(qml.CNOT(wires=[int(q1), int(q2)]))
            else:
                q = np.random.randint(num_qubits)
                if gate == 'H':
                    ops.append(qml.Hadamard(wires=q))
                elif gate == 'S':
                    ops.append(qml.S(wires=q))
                elif gate == 'X':
                    ops.append(qml.PauliX(wires=q))
                elif gate == 'Z':
                    ops.append(qml.PauliZ(wires=q))
        
        tape = qml.tape.QuantumTape(ops, [])
        U_qc = qml.matrix(tape)
        
        trace = np.trace(U_orig.conj().T @ U_qc)
        theta = np.angle(trace)
        diff = np.abs(U_orig - np.exp(1j * theta) * U_qc)
        
        if np.max(diff) <= 0.4 + 0.4 * np.max(np.abs(U_orig)):
            counter += 1
            qc_list.append(tape)
            
    return qc_list
