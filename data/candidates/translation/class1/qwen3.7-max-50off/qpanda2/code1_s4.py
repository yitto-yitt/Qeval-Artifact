# EVAL_META: task_id=1, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def run_bell_state_simulator():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.Measure(qubits[0], cbits[0])
    prog << pq.Measure(qubits[1], cbits[1])
    
    counts = qvm.run_with_configuration(prog, cbits, 1000)
    total = builtins.sum(counts.values())
    return {k: v / total for k, v in counts.items()}
