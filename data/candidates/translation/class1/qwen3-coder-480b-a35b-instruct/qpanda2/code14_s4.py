# EVAL_META: task_id=14, framework=qpanda2, class=1
import pyqpanda as pq
import math

def bell_each_shot():
    # Initialize quantum machine
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    # Create quantum program
    prog = pq.QProg()
    
    # Apply gates: H on qubit 0, then CNOT from qubit 0 to qubit 1
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    # Measure all qubits
    prog << pq.Measure(qubits[0], cbits[0]) << pq.Measure(qubits[1], cbits[1])
    
    # Run the program with configuration
    result = pq.run_with_configuration(machine, prog, cbits, 10)
    
    # Calculate total shots
    import builtins
    total_shots = builtins.sum(result.values())
    
    # Convert to probability distribution
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    # Free resources
    pq.destroy_quantum_machine(machine)
    
    return prob_dist
