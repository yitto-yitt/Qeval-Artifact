# EVAL_META: task_id=86, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    prog_full = pq.QProg()
    prog_full.insert(pq.H(qubits[0]))
    prog_full.insert(pq.CNOT(qubits[0], qubits[1]))
    prog_full.insert(pq.CNOT(qubits[1], qubits[2]))
    prog_full.insert(pq.CNOT(qubits[2], qubits[3]))
    prog_full.insert(pq.CNOT(qubits[3], qubits[4]))
    
    prog_limited = pq.QProg()
    prog_limited.insert(pq.H(qubits[0]))
    prog_limited.insert(pq.CNOT(qubits[0], qubits[1]))
    prog_limited.insert(pq.CNOT(qubits[1], qubits[2]))
    prog_limited.insert(pq.CNOT(qubits[2], qubits[3]))
    prog_limited.insert(pq.CNOT(qubits[3], qubits[4]))
    
    return prog_full, prog_limited

machine.finalize()
