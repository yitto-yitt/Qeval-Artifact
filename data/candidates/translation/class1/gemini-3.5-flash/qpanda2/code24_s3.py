# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def dj_algorithm(oracle):
    # Create a dummy program to extract qubits
    prog_temp = pq.QProg()
    prog_temp << oracle
    qubits = pq.get_all_used_qubits(prog_temp)
    
    # Sort qubits by physical address
    qubits = sorted(list(qubits), key=lambda q: q.get_phy_addr())
    n = len(qubits)
    
    # Initialize machine
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    # Allocate qubits and cbits on this machine to make them valid
    sim_qubits = machine.allocate_qubits(n)
    cbits = machine.allocate_cbits(n - 1)
    
    # Build the actual DJ program
    dj_prog = pq.QProg()
    
    # 1. Apply X to the last qubit
    dj_prog << pq.X(qubits[-1])
    
    # 2. Apply H to all qubits
    for q in qubits:
        dj_prog << pq.H(q)
        
    # 3. Apply oracle
    dj_prog << oracle
    
    # 4. Apply H to all qubits
    for q in qubits:
        dj_prog << pq.H(q)
        
    # 5. Measure first n-1 qubits
    for i in range(n - 1):
        dj_prog << pq.Measure(qubits[i], cbits[i])
        
    # Run configuration
    shots = 1000
    counts = machine.run_with_configuration(dj_prog, cbits, shots)
    
    # Calculate probabilities
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
