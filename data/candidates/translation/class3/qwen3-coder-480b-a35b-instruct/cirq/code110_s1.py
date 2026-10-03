# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    def operator_from_circuit(cirq_circuit):
        return cirq.unitary(cirq_circuit)
    
    def random_clifford(num_qubits):
        # Generate a random Clifford circuit using Cirq
        qubits = cirq.LineQubit.range(num_qubits)
        clifford_ops = []
        for _ in range(2 * num_qubits ** 2):
            if np.random.randint(2):
                i = np.random.randint(num_qubits)
                if np.random.randint(2):
                    clifford_ops.append(cirq.X(qubits[i]))
                else:
                    clifford_ops.append(cirq.Z(qubits[i]))
            else:
                i, j = np.random.choice(num_qubits, 2, replace=False)
                if np.random.randint(2):
                    clifford_ops.append(cirq.CNOT(qubits[i], qubits[j]))
                else:
                    clifford_ops.append(cirq.CZ(qubits[i], qubits[j]))
        return cirq.Circuit(clifford_ops)
    
    def equiv(op1, op2, rtol=0.4, atol=0.4):
        # Check if two operators are equivalent within tolerance
        return np.allclose(op1, op2, rtol=rtol, atol=atol)
    
    op_or = operator_from_circuit(circuit)
    num_qubits = len(circuit.all_qubits())
    qc_list = []
    counter = 0
    
    while counter < n:
        qc = random_clifford(num_qubits)
        op_qc = operator_from_circuit(qc)
        if equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
            
    return qc_list
