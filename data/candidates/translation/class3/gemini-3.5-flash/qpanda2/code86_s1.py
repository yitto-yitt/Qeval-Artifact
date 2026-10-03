# EVAL_META: task_id=86, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    # Full block (no block width restriction)
    prog_full = pq.QProg()
    prog_full << pq.H(q[0])
    
    circuit_full = pq.QCircuit()
    circuit_full << pq.CNOT(q[0], q[1]) \
                 << pq.CNOT(q[1], q[2]) \
                 << pq.CNOT(q[2], q[3]) \
                 << pq.CNOT(q[3], q[4])
    prog_full << circuit_full
    
    # Limited block (max_block_width of 3)
    prog_limited = pq.QProg()
    prog_limited << pq.H(q[0])
    
    circuit_lim1 = pq.QCircuit()
    circuit_lim1 << pq.CNOT(q[0], q[1]) \
                 << pq.CNOT(q[1], q[2])
                 
    circuit_lim2 = pq.QCircuit()
    circuit_lim2 << pq.CNOT(q[2], q[3]) \
                 << pq.CNOT(q[3], q[4])
                 
    prog_limited << circuit_lim1 << circuit_lim2
    
    return prog_full, prog_limited

# Manual Cleanup
machine.finalize()
