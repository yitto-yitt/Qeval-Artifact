# EVAL_META: task_id=56, framework=qpanda2, class=1
import pyqpanda as pq
import math

def not_gate(a):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    
    a = format(a, "08b")
    prog = pq.QProg()
    
    for i in range(8):
        if a[7-i] == "0":
            prog << pq.X(qubits[i])
    
    prog << pq.Measure_all(qubits, cbits)
    
    result = machine.run_with_configuration(prog, cbits, 1024)
    machine.finalize()
    
    # Calculate total shots
    import builtins
    total = builtins.sum(result.values())
    
    return {key: value / total for key, value in result.items()}
