# EVAL_META: task_id=118, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_c3sx_circuit():
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(4)
    
    prog = pq.QProg()
    prog.insert(pq.C3SX(qubits[0], qubits[1], qubits[2], qubits[3]))
    
    return prog, qubits
