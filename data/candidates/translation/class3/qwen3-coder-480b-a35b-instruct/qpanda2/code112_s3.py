# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import QProg, QCircuit, QGate, PauliOperator
from pyqpanda.utils import PauliOperator

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    prog = QProg()
    
    # Determine number of qubits needed
    num_qubits = len(pauli_strings[0])
    qubits_needed = qubits[:num_qubits]
    
    for pauli_string, time in zip(pauli_strings, times):
        # Convert pauli_string to PauliOperator
        pauli_dict = {}
        for i, pauli_char in enumerate(pauli_string):
            if pauli_char != 'I':
                pauli_dict[i] = pauli_char
        
        if pauli_dict:  # Only add if there's actually a non-identity operator
            pauli_op = PauliOperator(pauli_dict, 1.0)
            
            # Apply Trotter evolution - use qop evolution gate
            circuit = pq.QCircuit()
            # For each repetition
            for _ in range(reps):
                # Apply the evolution for the given time
                circuit.insert(pq.evolution(pauli_op, time / reps, qubits_needed))
            
            prog.insert(circuit)
    
    return prog

machine.finalize()
