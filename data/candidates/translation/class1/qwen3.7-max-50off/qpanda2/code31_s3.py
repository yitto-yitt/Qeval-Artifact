# EVAL_META: task_id=31, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def sampler_qiskit():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.measure_all(qubits, cbits)
    
    shots = 1024
    config = {"shots": shots, "seed": 42}
    counts = qvm.run_with_configuration(prog, cbits, config)
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
