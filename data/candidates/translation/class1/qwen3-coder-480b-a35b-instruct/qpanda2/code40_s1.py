# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    
    # Create quantum circuit
    prog = pq.QProg()
    
    # Initialize the state using U3 gates to prepare the desired state
    # We need to decompose the desired vector into appropriate rotations
    sv = np.array(desired_vector)
    
    # Create a circuit that prepares the desired state from |000>
    # This involves finding the appropriate sequence of rotations
    
    # First, we create a unitary matrix that transforms |000> to the desired state
    # We'll use the fact that any state can be prepared by applying appropriate rotations
    
    # Apply state preparation using U3 and CNOT gates
    # For a general 3-qubit state preparation, we need to construct the appropriate circuit
    
    # Reset all qubits to zero state (they start in |0>)
    # Then apply the necessary rotations to create the desired state
    
    # We will use the state preparation method available in pyqpanda
    prog.insert(pq.qist.init_state(qubits, sv))
    
    # Add measurements
    cbits = [machine.cAlloc() for _ in range(3)]
    for i in range(3):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    
    # Run the program
    result = machine.run_with_configuration(prog, cbits, 1024)  # Using 1024 shots as default
    
    # Process results
    total_shots = builtins.sum(result.values())
    prob_dist = {}
    for bitstring, count in result.items():
        prob_dist[bitstring] = count / total_shots
    
    machine.destroy_qvm()
    return prob_dist
