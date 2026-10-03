# EVAL_META: task_id=86, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    full_linear_block = pq.QCircuit()
    full_linear_block.insert(pq.CNOT(q[0], q[1]))
    full_linear_block.insert(pq.CNOT(q[1], q[2]))
    full_linear_block.insert(pq.CNOT(q[2], q[3]))
    full_linear_block.insert(pq.CNOT(q[3], q[4]))

    full_block = pq.QProg()
    full_block.insert(pq.H(q[0]))
    full_block.insert(full_linear_block)

    limited_linear_block_1 = pq.QCircuit()
    limited_linear_block_1.insert(pq.CNOT(q[0], q[1]))
    limited_linear_block_1.insert(pq.CNOT(q[1], q[2]))

    limited_linear_block_2 = pq.QCircuit()
    limited_linear_block_2.insert(pq.CNOT(q[2], q[3]))
    limited_linear_block_2.insert(pq.CNOT(q[3], q[4]))

    limited_block = pq.QProg()
    limited_block.insert(pq.H(q[0]))
    limited_block.insert(limited_linear_block_1)
    limited_block.insert(limited_linear_block_2)

    return full_block, limited_block

atexit.register(lambda: machine.finalize())
