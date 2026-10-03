# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_efficientSU2():
    circuit = pq.QCircuit()
    
    # Rotation layer 0
    for i in range(3):
        circuit << pq.RY(qubits[i], 0.0)
        circuit << pq.RZ(qubits[i], 0.0)
        
    # Barrier
    circuit << pq.BARRIER(qubits)
    
    # Entanglement layer 0
    circuit << pq.CNOT(qubits[0], qubits[1])
    circuit << pq.CNOT(qubits[1], qubits[2])
    
    # Barrier
    circuit << pq.BARRIER(qubits)
    
    # Rotation layer 1
    for i in range(3):
        circuit << pq.RY(qubits[i], 0.0)
        circuit << pq.RZ(qubits[i], 0.0)
        
    return circuit

# Manual Cleanup
machine.finalize()
