# EVAL_META: task_id=86, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    # Full block (no limit)
    prog_full = pq.QProg()
    prog_full << pq.H(qubits[0])
    block_full = pq.QCircuit()
    block_full << pq.CNOT(qubits[0], qubits[1])
    block_full << pq.CNOT(qubits[1], qubits[2])
    block_full << pq.CNOT(qubits[2], qubits[3])
    block_full << pq.CNOT(qubits[3], qubits[4])
    prog_full << block_full

    # Limited block (max_block_width=3)
    prog_limited = pq.QProg()
    prog_limited << pq.H(qubits[0])
    block1 = pq.QCircuit()
    block1 << pq.CNOT(qubits[0], qubits[1])
    block1 << pq.CNOT(qubits[1], qubits[2])
    prog_limited << block1
    block2 = pq.QCircuit()
    block2 << pq.CNOT(qubits[2], qubits[3])
    block2 << pq.CNOT(qubits[3], qubits[4])
    prog_limited << block2

    return prog_full, prog_limited

if __name__ == "__main__":
    machine.finalize()
