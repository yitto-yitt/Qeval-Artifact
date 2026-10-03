# EVAL_META: task_id=71, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_csx01_h1():
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(3)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CU(qubits[0], qubits[1], pq.PI/2, 0, 0))
    prog.insert(pq.H(qubits[1]))
    
    return prog, qubits
