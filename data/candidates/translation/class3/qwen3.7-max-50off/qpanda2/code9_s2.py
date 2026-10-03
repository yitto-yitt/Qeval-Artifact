# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_efficientSU2():
    circ = pq.QCircuit()
    
    for q in qubits:
        circ << pq.RY(q, 0.0)
        circ << pq.RZ(q, 0.0)
        
    circ << pq.Barrier(qubits)
    
    circ << pq.CNOT(qubits[0], qubits[1])
    circ << pq.CNOT(qubits[1], qubits[2])
    
    circ << pq.Barrier(qubits)
    
    for q in qubits:
        circ << pq.RY(q, 0.0)
        circ << pq.RZ(q, 0.0)
        
    return circ

machine.finalize()
