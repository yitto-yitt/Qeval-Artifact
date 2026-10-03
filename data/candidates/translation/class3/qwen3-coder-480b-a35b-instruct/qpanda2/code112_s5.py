# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)  # Assuming max 10 qubits based on input

def create_product_formula_circuit(pauli_strings, times, order, reps):
    qvm = machine
    n_qubits = len(pauli_strings[0])
    qubits_local = qubits[:n_qubits]
    
    prog = pq.QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        # Convert Pauli string to Hamiltonian terms
        hamiltonian_terms = []
        
        for i, pauli_op in enumerate(pauli_string):
            if pauli_op == 'X':
                hamiltonian_terms.append((pq.PauliOperator({f"X{i}": 1}), time))
            elif pauli_op == 'Y':
                hamiltonian_terms.append((pq.PauliOperator({f"Y{i}": 1}), time))
            elif pauli_op == 'Z':
                hamiltonian_terms.append((pq.PauliOperator({f"Z{i}": 1}), time))
            elif pauli_op == 'I':
                continue  # Identity does not contribute to evolution
        
        # If there are terms to evolve
        if hamiltonian_terms:
            # For Lie-Trotter we apply each term separately
            for pauli_op, t in hamiltonian_terms:
                # Apply Trotterized evolution - for each term in the Hamiltonian
                for _ in range(reps):
                    # Simple implementation of exp(-i*t*P) where P is a Pauli operator
                    # For single Pauli terms, we can use the formula directly
                    if str(pauli_op).strip() != "I":  # Not identity
                        # Extract the qubit index and Pauli type
                        pauli_str = str(pauli_op)
                        # Parse the operator to get the qubit and Pauli type
                        parsed_ops = pauli_op.get_terms()
                        for term, coeff in parsed_ops.items():
                            # term is like {qubit_index: pauli_type}
                            for qubit_idx, pauli_type in term.items():
                                # Apply the evolution based on Pauli type
                                if pauli_type == 'X':
                                    prog << pq.RX(qubits_local[qubit_idx], -2 * t / reps)
                                elif pauli_type == 'Y':
                                    prog << pq.RY(qubits_local[qubit_idx], -2 * t / reps)
                                elif pauli_type == 'Z':
                                    prog << pq.RZ(qubits_local[qubit_idx], -2 * t / reps)
    
    return prog

# Clean up
machine.finalize()
