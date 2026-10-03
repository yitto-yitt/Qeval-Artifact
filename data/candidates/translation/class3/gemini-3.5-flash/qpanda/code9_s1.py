# EVAL_META: task_id=9, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_efficientSU2():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    
    prog = pq.QProg()
    params = [pq.var(0.0) for _ in range(12)]
    
    # Initial SU(2) layer
    prog << pq.RY(qubits[0], params[0])
    prog << pq.RZ(qubits[0], params[1])
    prog << pq.RY(qubits[1], params[2])
    prog << pq.RZ(qubits[1], params[3])
    prog << pq.RY(qubits[2], params[4])
    prog << pq.RZ(qubits[2], params[5])
    
    prog << pq.BARRIER(qubits)
    
    # Entanglement layer (reverse_linear)
    prog << pq.CNOT(qubits[2], qubits[1])
    prog << pq.CNOT(qubits[1], qubits[0])
    
    prog << pq.BARRIER(qubits)
    
    # Final SU(2) layer
    prog << pq.RY(qubits[0], params[6])
    prog << pq.RZ(qubits[0], params[7])
    prog << pq.RY(qubits[1], params[8])
    prog << pq.RZ(qubits[1], params[9])
    prog << pq.RY(qubits[2], params[10])
    prog << pq.RZ(qubits[2], params[11])
    
    return prog
