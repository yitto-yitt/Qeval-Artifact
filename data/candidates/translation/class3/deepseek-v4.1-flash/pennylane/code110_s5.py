# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    U_orig = qml.matrix(circuit)
    num_qubits = int(np.log2(U_orig.shape[0]))
    
    def random_clifford_circuit():
        ops = []
        num_gates = np.random.randint(1, 10 * num_qubits + 1)
        for _ in range(num_gates):
            gate_type = np.random.choice(['H', 'S', 'Sdg', 'X', 'Y', 'Z', 'CNOT'])
            if gate_type == 'H':
                wire = np.random.randint(num_qubits)
                ops.append(qml.Hadamard(wire))
            elif gate_type == 'S':
                wire = np.random.randint(num_qubits)
                ops.append(qml.S(wire))
            elif gate_type == 'Sdg':
                wire = np.random.randint(num_qubits)
                ops.append(qml.adjoint(qml.S(wire)))
            elif gate_type == 'X':
                wire = np.random.randint(num_qubits)
                ops.append(qml.PauliX(wire))
            elif gate_type == 'Y':
                wire = np.random.randint(num_qubits)
                ops.append(qml.PauliY(wire))
            elif gate_type == 'Z':
                wire = np.random.randint(num_qubits)
                ops.append(qml.PauliZ(wire))
            elif gate_type == 'CNOT':
                if num_qubits >= 2:
                    control = np.random.randint(num_qubits)
                    target = np.random.randint(num_qubits)
                    while target == control:
                        target = np.random.randint(num_qubits)
                    ops.append(qml.CNOT([control, target]))
        return QuantumScript(ops, [])
    
    def is_equivalent(U1, U2, rtol=0.4, atol=0.4):
        dim = U1.shape[0]
        trace = np.trace(U1.conj().T @ U2)
        phase = trace / dim
        return np.allclose(U1, phase * U2, rtol=rtol, atol=atol)
    
    qc_list = []
    counter = 0
    while counter < n:
        qc = random_clifford_circuit()
        U_qc = qml.matrix(qc)
        if is_equivalent(U_orig, U_qc, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
