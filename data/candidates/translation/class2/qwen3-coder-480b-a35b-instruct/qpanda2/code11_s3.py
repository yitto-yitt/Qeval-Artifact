# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    # Convert the input circuit to pyQPanda format if needed
    # Assuming circuit is already in pyQPanda format or can be processed
    prog = pq.QProg()
    
    # Extract quantum and classical registers from the circuit if available
    # If circuit is a pyQPanda program, use it directly
    if hasattr(circuit, 'qubits') and hasattr(circuit, 'cbits'):
        prog << circuit
    else:
        # If circuit is QProg, use it directly
        prog = circuit
    
    # Get the state vector using pyQPanda's functionality
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qvec = machine.qAlloc_many(len(prog.get_used_qubits()))
    
    # Execute the program and get state vector
    result = pq.get_state_vector(prog, machine)
    pq.destroy_quantum_machine(machine)
    
    return result
