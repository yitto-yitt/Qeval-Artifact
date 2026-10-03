# EVAL_META: task_id=31, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.Measure(qubits[0], cbits[0])
    prog << pq.Measure(qubits[1], cbits[1])
    
    try:
        machine.set_seed(42)
    except Exception:
        pass
        
    counts = machine.run_with_configuration(prog, cbits, 1000)
    total = builtins.sum(counts.values())
    
    return {k: v / total for k, v in counts.items()}
