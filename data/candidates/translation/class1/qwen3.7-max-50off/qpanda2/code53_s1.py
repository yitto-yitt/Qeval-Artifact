# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def xor_gate(a, b):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    
    prog = pq.QProg()
    circ = pq.QCircuit()
    
    xor_val = a ^ b
    for i in range(8):
        if (xor_val >> i) & 1:
            circ << pq.X(qubits[i])
            
    prog << circ
    for i in range(8):
        prog << pq.Measure(qubits[i], cbits[i])
        
    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(counts.values())
    
    result = {}
    for k, v in counts.items():
        key_str = str(k)
        if len(key_str) < 8:
            key_str = key_str.zfill(8)
        result[key_str] = v / total
        
    return result
