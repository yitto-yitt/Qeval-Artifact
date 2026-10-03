# EVAL_META: task_id=71, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_csx01_h1():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.SX(q[1]).control([q[0]])
    prog << pq.H(q[1])
    prog.machine = machine  # Keep machine alive to prevent garbage collection of qubits
    return prog
