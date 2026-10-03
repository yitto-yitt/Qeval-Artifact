# EVAL_META: task_id=62, framework=qpanda, class=2
import pyqpanda3.core as pq

_machines = []

def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    machine = pq.CPUQVM()
    machine.init_qvm()
    _machines.append(machine)
    qubits = machine.qAlloc_many(num_qubits)
    
    prog = pq.QProg()
    for i in range(len(basis)):
        if state[i] == 1:
            prog << pq.X(qubits[i])
        if basis[i] == 1:
            prog << pq.H(qubits[i])
            
    return prog
