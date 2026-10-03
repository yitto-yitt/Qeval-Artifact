# EVAL_META: task_id=24, framework=qpanda, class=1
import pyqpanda3.core as pq

def dj_algorithm(oracle):
    machine = pq.get_global_machine()
    
    # Retrieve and sort the qubits used in the oracle
    qubits = sorted(list(oracle.get_used_qubits()), key=lambda q: q.get_phy_addr())
    
    prog = pq.QProg()
    # Put the output qubit in state |1>
    prog << pq.X(qubits[-1])
    
    # Apply Hadamard gates to all qubits
    for q in qubits:
        prog << pq.H(q)
        
    # Apply the oracle
    prog << oracle
    
    # Apply Hadamard gates to all qubits again
    for q in qubits:
        prog << pq.H(q)
        
    # Measure the first n-1 qubits. 
    # Reverse the list to match Qiskit's little-endian bitstring ordering.
    measure_qubits = qubits[:-1][::-1]
    
    machine.directly_run(prog)
    prob_dict = machine.get_prob_dict(measure_qubits, -1)
    
    # Filter out zero probabilities to match the behavior of get_counts()
    return {key: val for key, val in prob_dict.items() if val > 1e-9}
