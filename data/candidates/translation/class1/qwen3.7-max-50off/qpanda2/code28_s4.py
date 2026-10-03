# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def visualize_bell_states():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    
    q1 = machine.qAlloc_many(2)
    c1 = machine.cAlloc_many(2)
    prog1 = pq.QProg()
    prog1.insert(pq.H(q1[0]))
    prog1.insert(pq.CNOT(q1[0], q1[1]))
    prog1.insert(pq.measure_all(q1, c1))
    
    q2 = machine.qAlloc_many(2)
    c2 = machine.cAlloc_many(2)
    prog2 = pq.QProg()
    prog2.insert(pq.X(q2[0]))
    prog2.insert(pq.H(q2[0]))
    prog2.insert(pq.CNOT(q2[0], q2[1]))
    prog2.insert(pq.measure_all(q2, c2))
    
    shots = 1000
    counts1 = machine.run_with_configuration(prog1, c1, shots)
    counts2 = machine.run_with_configuration(prog2, c2, shots)
    
    total1 = builtins.sum(counts1.values())
    total2 = builtins.sum(counts2.values())
    
    phi_plus_dist = {k: v / total1 for k, v in counts1.items()}
    phi_minus_dist = {k: v / total2 for k, v in counts2.items()}
    
    pq.destroy_quantum_machine(machine)
    
    return {
        "phi_plus": phi_plus_dist,
        "phi_minus": phi_minus_dist
    }
