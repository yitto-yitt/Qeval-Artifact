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
    
    # Initialize the state
    # In pyqpanda, we need to decompose the desired vector into gates
    # Using U3 gates to prepare the arbitrary state
    sv = pq.StateVec.from_complex_array(np.array(desired_vector))
    init_prog = pq.bind_datatype_to_gate_type(pq.q initState, sv, qubits)
    
    # Since pyqpanda doesn't have a direct initialize gate like Qiskit,
    # we need to construct the state preparation manually
    # We'll create a circuit that prepares the desired state
    
    # First, let's try to use the quantum state preparation method
    prog << init_prog
    
    # Measure all qubits
    cbits = [machine.cAlloc() for _ in range(3)]
    for i in range(3):
        prog << pq.Measure(qubits[i], cbits[i])
        
    # Run the program
    shots = 10000  # Equivalent to sampler behavior
    result = machine.run_with_configuration(prog, cbits, shots)
    
    # Convert results to probability distribution
    total_shots = shots
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
        
    machine.finalize()
    return prob_dist
