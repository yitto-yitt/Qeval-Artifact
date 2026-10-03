# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *

# Global QVM
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(30)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubit_list = q[:num_qubits]
    
    qc = QCircuit()
    for pauli_string, time in zip(pauli_strings, times):
        terms = []
        for i, char in enumerate(reversed(pauli_string)):
            if char != 'I':
                terms.append(f"{char}{i}")
        qpanda_pauli_str = " ".join(terms)
        
        op = PauliOperator(qpanda_pauli_str, 1.0)
        theta = 2.0 * time / reps
        
        for _ in range(reps):
            step_circuit = exp(qubit_list, op, theta)
            qc << step_circuit
            
    return qc

machine.finalize()
