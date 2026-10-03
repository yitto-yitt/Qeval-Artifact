# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def xor_gate(a, b):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(8)
    cubits = machine.cAlloc_many(8)
    prog = pq.QProg()
    
    for i in range(8):
        if (a >> i) & 1:
            prog << pq.X(qubits[i])
    for i in range(8):
        if (b >> i) & 1:
            prog << pq.X(qubits[i])
            
    for i in range(8):
        prog << pq.Measure(qubits[i], cubits[i])
        
    result = pq.run_with_configuration(prog, machine, 1000)
    
    total = builtins.sum(result.values())
    return {k: v / total for k, v in result.items()}
