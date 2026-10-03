# EVAL_META: task_id=56, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def not_gate(a):
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    
    prog = pq.QProg()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            prog << pq.X(qubits[i])
            
    for i in range(8):
        prog << pq.Measure(qubits[i], cbits[i])
        
    counts = pq.run_with_configuration(prog, cbits, 1000)
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
