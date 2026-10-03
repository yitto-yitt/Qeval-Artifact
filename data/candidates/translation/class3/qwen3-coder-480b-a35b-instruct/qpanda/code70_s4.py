# EVAL_META: task_id=70, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(3)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CSWAP(qubits[0], qubits[1], qubits[2]))
    prog.insert(pq.H(qubits[1]))
    prog.insert(pq.CSdag(qubits[1], qubits[0]))
    
    return prog, qubits
