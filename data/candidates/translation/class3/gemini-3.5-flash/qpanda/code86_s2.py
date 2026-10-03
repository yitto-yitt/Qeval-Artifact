# EVAL_META: task_id=86, framework=qpanda, class=3
import pyqpanda3.core as pq

def collect_linear_blocks_with_and_without_limit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(5)
    
    # Full block program
    full_prog = pq.QProg()
    full_prog << pq.H(q[0])
    
    full_linear_circuit = pq.QCircuit()
    full_linear_circuit << pq.CNOT(q[0], q[1]) \
                        << pq.CNOT(q[1], q[2]) \
                        << pq.CNOT(q[2], q[3]) \
                        << pq.CNOT(q[3], q[4])
    full_prog << full_linear_circuit
    
    # Limited block program
    limited_prog = pq.QProg()
    limited_prog << pq.H(q[0])
    
    block1 = pq.QCircuit()
    block1 << pq.CNOT(q[0], q[1]) << pq.CNOT(q[1], q[2])
    
    block2 = pq.QCircuit()
    block2 << pq.CNOT(q[2], q[3]) << pq.CNOT(q[3], q[4])
    
    limited_prog << block1 << block2
    
    return full_prog, limited_prog
