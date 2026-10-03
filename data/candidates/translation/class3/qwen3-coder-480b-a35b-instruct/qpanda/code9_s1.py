# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda import *

def create_efficientSU2():
    machine = init(QMachineType.CPU)
    qubits = machine.qAlloc_many(3)
    circuit = QCircuit()
    
    # First layer of single-qubit rotations
    for i in range(3):
        circuit.insert(RY(qubits[i], 0))
        circuit.insert(RZ(qubits[i], 0))
    
    # Barrier
    circuit.insert(BARRIER(machine))
    
    # Entangling layer
    circuit.insert(CNOT(qubits[0], qubits[1]))
    circuit.insert(CNOT(qubits[1], qubits[2]))
    
    # Barrier
    circuit.insert(BARRIER(machine))
    
    # Second layer of single-qubit rotations
    for i in range(3):
        circuit.insert(RY(qubits[i], 0))
        circuit.insert(RZ(qubits[i], 0))
    
    # Barrier
    circuit.insert(BARRIER(machine))
    
    finalize()
    return circuit
