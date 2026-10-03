# EVAL_META: task_id=86, framework=qpanda, class=3
import pyqpanda3.core as pq

def collect_linear_blocks_with_and_without_limit():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(5)
    
    # Full block (no limit)
    prog_full = pq.QProg()
    prog_full << pq.H(qubits[0])
    
    circuit_full = pq.QCircuit()
    circuit_full << pq.CNOT(qubits[0], qubits[1])
    circuit_full << pq.CNOT(qubits[1], qubits[2])
    circuit_full << pq.CNOT(qubits[2], qubits[3])
    circuit_full << pq.CNOT(qubits[3], qubits[4])
    prog_full << circuit_full
    
    # Limited block (max_block_width of 3)
    prog_limited = pq.QProg()
    prog_limited << pq.H(qubits[0])
    
    circuit_lim1 = pq.QCircuit()
    circuit_lim1 << pq.CNOT(qubits[0], qubits[1])
    circuit_lim1 << pq.CNOT(qubits[1], qubits[2])
    
    circuit_lim2 = pq.QCircuit()
    circuit_lim2 << pq.CNOT(qubits[2], qubits[3])
    circuit_lim2 << pq.CNOT(qubits[3], qubits[4])
    
    prog_limited << circuit_lim1
    prog_limited << circuit_lim2
    
    return prog_full, prog_limited
