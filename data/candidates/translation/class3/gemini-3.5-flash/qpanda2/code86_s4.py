# EVAL_META: task_id=86, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    prog_full = pq.QProg()
    prog_full << pq.H(q[0])
    
    block_full = pq.QCircuit()
    block_full << pq.CNOT(q[0], q[1]) \
               << pq.CNOT(q[1], q[2]) \
               << pq.CNOT(q[2], q[3]) \
               << pq.CNOT(q[3], q[4])
    prog_full << block_full
    
    prog_limited = pq.QProg()
    prog_limited << pq.H(q[0])
    
    block1 = pq.QCircuit()
    block1 << pq.CNOT(q[0], q[1]) \
           << pq.CNOT(q[1], q[2])
           
    block2 = pq.QCircuit()
    block2 << pq.CNOT(q[2], q[3]) \
           << pq.CNOT(q[3], q[4])
           
    prog_limited << block1 << block2
    
    return prog_full, prog_limited

machine.finalize()
