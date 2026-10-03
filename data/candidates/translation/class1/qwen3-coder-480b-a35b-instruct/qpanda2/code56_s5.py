# EVAL_META: task_id=56, framework=qpanda2, class=1
import pyqpanda as pq
import math

def not_gate(a):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    
    prog = pq.QProg()
    
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            prog.insert(pq.X(qubits[i]))
    
    prog.insert(pq.MeasureAll(qubits, cbits))
    
    result = machine.run_with_configuration(prog, cbits, 1024)
    
    # Calculate total shots
    import builtins
    total_shots = builtins.sum(result.values())
    
    # Convert to probability distribution
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    machine.finalize()
    return prob_dist
