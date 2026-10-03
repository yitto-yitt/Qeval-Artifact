# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda import *
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    # Convert Qiskit circuit to pyQPanda circuit
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(circuit.num_qubits)
    cbits = qvm.cAlloc_many(circuit.num_qubits)
    
    # Create original circuit in pyQPanda
    prog_orig = QProg()
    prog_orig.insert(circuit_to_qprog(circuit, qubits, cbits))
    
    # Get unitary of original circuit
    U_orig = get_unitary(prog_orig, qubits)
    
    qc_list = []
    counter = 0
    
    while counter < n:
        # Generate random Clifford circuit
        clifford_circuit = random_clifford_circuit(circuit.num_qubits)
        prog_test = QProg()
        prog_test.insert(circuit_to_qprog(clifford_circuit, qubits, cbits))
        
        # Get unitary of test circuit
        U_test = get_unitary(prog_test, qubits)
        
        # Check equivalence with tolerance
        if np.allclose(U_test, U_orig, rtol=0.4, atol=0.4):
            qc_list.append(clifford_circuit)
            counter += 1
            
    qvm.finalize()
    return qc_list

def circuit_to_qprog(circuit, qubits, cbits):
    # Helper function to convert Qiskit-style operations to pyQPanda
    prog = QProg()
    for gate_name, qubit_indices in circuit:
        if gate_name == 'h':
            prog.insert(H(qubits[qubit_indices[0]]))
        elif gate_name == 's':
            prog.insert(S(qubits[qubit_indices[0]]))
        elif gate_name == 'x':
            prog.insert(X(qubits[qubit_indices[0]]))
        elif gate_name == 'y':
            prog.insert(Y(qubits[qubit_indices[0]]))
        elif gate_name == 'z':
            prog.insert(Z(qubits[qubit_indices[0]]))
        elif gate_name == 'cx':
            prog.insert(CNOT(qubits[qubit_indices[0]], qubits[qubit_indices[1]]))
    return prog

def random_clifford_circuit(num_qubits):
    # Generate a random Clifford circuit
    clifford_gates = ['h', 's', 'x', 'y', 'z', 'cx']
    circuit = []
    for _ in range(10*num_qubits):  # Arbitrary depth
        gate = np.random.choice(clifford_gates)
        if gate == 'cx':
            if num_qubits > 1:
                q1, q2 = np.random.choice(num_qubits, 2, replace=False)
                circuit.append((gate, [q1, q2]))
        else:
            q = np.random.randint(num_qubits)
            circuit.append((gate, [q]))
    return circuit
