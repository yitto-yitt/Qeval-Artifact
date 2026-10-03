# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    qubits = sorted(list(circuit.all_qubits()))
    num_qubits = len(qubits)
    if num_qubits == 0:
        return [cirq.Circuit() for _ in range(n)]
        
    U_orig = cirq.unitary(circuit)
    
    qc_list = []
    counter = 0
    
    gates_1q = [cirq.X, cirq.Y, cirq.Z, cirq.H, cirq.S]
    
    while counter < n:
        if np.random.rand() < 0.5 or counter > n * 10:
            qc = circuit.copy()
            for _ in range(np.random.randint(1, 4)):
                q = np.random.choice(qubits)
                gate = np.random.choice([cirq.X, cirq.Y, cirq.Z, cirq.H])
                qc.append(gate(q))
                qc.append(gate(q))
        else:
            qc = cirq.Circuit()
            depth = np.random.randint(1, 5 * num_qubits + 2)
            for _ in range(depth):
                for q in qubits:
                    if np.random.rand() < 0.5:
                        gate = np.random.choice(gates_1q)
                        qc.append(gate(q))
                if num_qubits > 1 and np.random.rand() < 0.5:
                    q1, q2 = np.random.choice(qubits, 2, replace=False)
                    qc.append(cirq.CNOT(q1, q2))
                    
        U_qc = cirq.unitary(qc)
        
        trace_val = np.trace(U_orig @ U_qc.conj().T)
        if np.abs(trace_val) > 1e-10:
            phase = trace_val / np.abs(trace_val)
        else:
            phase = 1.0
            
        if np.allclose(U_orig, phase * U_qc, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
            
    return qc_list
