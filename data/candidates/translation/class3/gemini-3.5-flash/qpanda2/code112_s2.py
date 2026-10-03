# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
# Allocate a pool of qubits globally to prevent premature garbage collection
global_qubits = machine.qAlloc_many(100)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    prog = pq.QProg()
    if not pauli_strings:
        return prog
        
    N = len(pauli_strings[0])
    
    # Construct QVec for the active qubits
    qvec = pq.QVec()
    for i in range(N):
        qvec.push_back(global_qubits[i])
        
    for pauli_string, time in zip(pauli_strings, times):
        term_str_list = []
        for i, char in enumerate(pauli_string):
            if char != 'I':
                qubit_idx = N - 1 - i
                term_str_list.append(f"{char}{qubit_idx}")
                
        if not term_str_list:
            continue
            
        term_str = " ".join(term_str_list)
        op = pq.QPauliOperator({term_str: 1.0})
        
        step_time = time / reps
        for _ in range(reps):
            circuit = pq.exp(qvec, op, step_time)
            prog << circuit
            
    return prog

# Manual Cleanup
machine.finalize()
