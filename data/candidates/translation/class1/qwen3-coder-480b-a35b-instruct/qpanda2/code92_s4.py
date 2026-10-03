# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq
from pyqpanda import *
import numpy as np

def calculate_stabilizer_state_info():
    # Initialize QVM
    qvm = pq.QVM()
    qvm.init_qvm()
    
    # Allocate qubits
    qubits = qvm.qAlloc_many(2)
    
    # Create quantum program
    prog = pq.QProg()
    
    # Apply H gate to first qubit
    prog.insert(pq.H(qubits[0]))
    # Apply CNOT gate
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    
    # Measure all qubits to get the state information
    result = qvm.run_with_configuration(prog, qubits, 1000)
    
    # Calculate probabilities based on the ideal state
    # For Phi+ Bell state |00> + |11>, we expect equal probability for |00> and |11>
    # In QPanda, we need to simulate this differently since there's no direct stabilizer state
    # We'll create the equivalent by running measurements and calculating theoretically
    
    # The Phi+ state is (|00> + |11>)/sqrt(2), so probabilities should be 0.5 for |00> and |11>
    # Simulate by creating the quantum state vector
    qvm1 = pq.QVM()
    qvm1.init_qvm()
    qubits1 = qvm1.qAlloc_many(2)
    prog1 = pq.QProg()
    prog1.insert(pq.H(qubits1[0])).insert(pq.CNOT(qubits1[0], qubits1[1]))
    
    # Get the quantum state vector
    qvm1.directly_run(prog1)
    state_vector = qvm1.get_quantum_state()
    
    # Calculate probabilities from the state vector
    probs = []
    for i in range(len(state_vector)):
        prob = abs(state_vector[i])**2
        probs.append(prob)
    
    # Create probability dictionary
    prob_dict = {}
    for i in range(len(probs)):
        # Convert index to binary string
        binary_str = format(i, f'0{2}b')
        prob_dict[binary_str] = probs[i]
    
    qvm.finalize()
    qvm1.finalize()
    
    # Since we know the theoretical result for Phi+ state
    # It should have equal probability for |00> and |11>
    theoretical_result = {'00': 0.5, '11': 0.5}
    
    # Verify against theoretical result
    actual_probs = {}
    total_prob = sum(probs)
    for i, prob in enumerate(probs):
        if prob > 1e-6:  # Only include non-negligible probabilities
            binary_str = format(i, f'0{2}b')
            actual_probs[binary_str] = prob
    
    return actual_probs
