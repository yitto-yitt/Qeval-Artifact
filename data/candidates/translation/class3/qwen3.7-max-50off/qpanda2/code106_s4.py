# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def compose_cnot_dihedral():
    circ1 = pq.QCircuit()
    circ1 << pq.CNOT(qubits[0], qubits[1])
    circ1 << pq.T(qubits[0])
    
    circ2 = pq.QCircuit()
    circ2 << pq.CNOT(qubits[0], qubits[1])
    circ2 << pq.T(qubits[0])
    circ2 << pq.X(qubits[1])
    
    composed_circ = pq.QCircuit()
    composed_circ << circ1 << circ2
    
    return composed_circ

machine.finalize()
