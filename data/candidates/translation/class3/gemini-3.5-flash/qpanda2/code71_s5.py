# EVAL_META: task_id=71, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.SX(q[1]).control([q[0]])
    prog << pq.H(q[1])
    return prog

if __name__ == "__main__":
    machine.finalize()
