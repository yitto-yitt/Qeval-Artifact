# EVAL_META: task_id=14, framework=qpanda2, class=1
import pyqpanda as pq
import math

def bell_each_shot():
    # Initialize quantum machine
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    # Create quantum program
    prog = pq.QProg()
    
    # Apply gates: H on q[0], then CNOT from q[0] to q[1]
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    
    # Measure all qubits
    prog << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])

    # Run the program
    result = pq.run_with_configuration(machine, prog, c, 10)
    
    # Calculate total shots
    import builtins
    total_shots = builtins.sum(result.values())
    
    # Convert to probability distribution
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    # Destroy quantum machine
    pq.destroy_quantum_machine(machine)
    
    return prob_dist
