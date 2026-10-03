# EVAL_META: task_id=86, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    prog1 = pq.QProg()
    prog1 << pq.H(qubits[0])
    prog1 << pq.CNOT(qubits[0], qubits[1])
    prog1 << pq.CNOT(qubits[1], qubits[2])
    prog1 << pq.CNOT(qubits[2], qubits[3])
    prog1 << pq.CNOT(qubits[3], qubits[4])
    
    prog2 = pq.QProg()
    prog2 << pq.H(qubits[0])
    prog2 << pq.CNOT(qubits[0], qubits[1])
    prog2 << pq.CNOT(qubits[1], qubits[2])
    prog2 << pq.CNOT(qubits[2], qubits[3])
    prog2 << pq.CNOT(qubits[3], qubits[4])
    
    return prog1, prog2

machine.finalize()
