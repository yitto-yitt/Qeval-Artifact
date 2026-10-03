# EVAL_META: task_id=38, framework=qpanda, class=3
import pyqpanda3 as pq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    prog = pq.QProg()
    
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CRZ(qubits[0], qubits[1], theta))
    prog.insert(pq.H(qubits[1]))
    prog.insert(pq.CRY(qubits[1], qubits[0], theta))
    
    return prog, qubits
