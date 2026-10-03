# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_efficientSU2():
    circ = pq.QCircuit()
    
    # Initial layer
    for i in range(3):
        circ << pq.RY(qubits[i], 0.0) << pq.RZ(qubits[i], 0.0)
    circ << pq.Barrier(qubits)
    
    # Entanglement layer
    circ << pq.CNOT(qubits[0], qubits[1]) << pq.CNOT(qubits[1], qubits[2])
    circ << pq.Barrier(qubits)
    
    # Rep 1
    for i in range(3):
        circ << pq.RY(qubits[i], 0.0) << pq.RZ(qubits[i], 0.0)
        
    return circ

machine.finalize()
