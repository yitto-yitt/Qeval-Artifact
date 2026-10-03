# EVAL_META: task_id=69, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    circ = pq.QCircuit()
    
    # H on 0
    circ << pq.H(q[0])
    
    # CS on 0, 1 (Decomposed into U1 and CNOT)
    circ << pq.U1(q[0], np.pi/4)
    circ << pq.U1(q[1], np.pi/4)
    circ << pq.CNOT(q[0], q[1])
    circ << pq.U1(q[1], -np.pi/4)
    circ << pq.CNOT(q[0], q[1])
    
    # H on 1
    circ << pq.H(q[1])
    
    # CSdg on 1, 0 (Decomposed into U1 and CNOT)
    circ << pq.U1(q[1], -np.pi/4)
    circ << pq.U1(q[0], -np.pi/4)
    circ << pq.CNOT(q[1], q[0])
    circ << pq.U1(q[0], np.pi/4)
    circ << pq.CNOT(q[1], q[0])
    
    prog = pq.QProg()
    prog << circ
    return prog

machine.finalize()
