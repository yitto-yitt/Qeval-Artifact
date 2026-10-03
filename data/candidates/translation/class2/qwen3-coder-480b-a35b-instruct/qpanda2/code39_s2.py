# EVAL_META: task_id=39, framework=qpanda2, class=2
import pyqpanda as pq

def create_uniform_superposition(n):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n)
    
    prog = pq.QProg()
    for i in range(n):
        prog << pq.H(qubits[i])
    
    statevector = pq.get_state_vector(prog, machine)
    machine.destroy()
    return statevector
