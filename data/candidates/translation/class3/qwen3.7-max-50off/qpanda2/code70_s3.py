# EVAL_META: task_id=70, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    prog = pq.QProg()
    
    # H on qubit 0
    prog << pq.H(q[0])
    
    # CSWAP (Fredkin) on control 0, targets 1 and 2
    prog << pq.CNOT(q[2], q[1])
    prog << pq.Toffoli(q[0], q[1], q[2])
    prog << pq.CNOT(q[2], q[1])
    
    # H on qubit 1
    prog << pq.H(q[1])
    
    # Controlled-S dagger on control 1, target 0
    sdg_gate = pq.S(q[0]).dagger()
    csdg_gate = sdg_gate.control([q[1]])
    prog << csdg_gate
    
    return prog

machine.finalize()
