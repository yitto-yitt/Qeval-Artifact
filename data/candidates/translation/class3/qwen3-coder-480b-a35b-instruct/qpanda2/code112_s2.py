# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import QProg, QCircuit, QGate, PauliOperator
from pyqpanda.Algorithm import QPE, QAOA
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    prog = QProg()
    
    # Calculate total number of qubits needed
    num_qubits = len(pauli_strings[0])
    local_qubits = qubits[:num_qubits]
    
    # Process each Pauli string with its corresponding time
    for pauli_string, time in zip(pauli_strings, times):
        # Convert Pauli string to PauliOperator
        pauli_dict = {}
        for i, pauli_char in enumerate(pauli_string):
            if pauli_char != 'I':
                pauli_dict[i] = pauli_char
        
        if pauli_dict:  # Only add evolution if there are non-identity terms
            hamiltonian = PauliOperator(pauli_dict, 1.0)
            
            # Apply Trotter evolution - repeat reps times
            for _ in range(reps):
                # Simple implementation of Lie-Trotter: evolve each term separately
                for pos, pauli_op in pauli_dict.items():
                    if pauli_op == 'X':
                        prog << pq.RX(local_qubits[pos], 2 * time)
                    elif pauli_op == 'Y':
                        prog << pq.RY(local_qubits[pos], 2 * time)
                    elif pauli_op == 'Z':
                        prog << pq.RZ(local_qubits[pos], 2 * time)
    
    return prog

machine.finalize()
