# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, RY, RZ, CNOT, BARRIER, Parameter

def create_efficientSU2():
    qubits = [Qubit(i) for i in range(3)]
    params = [Parameter(f"theta[{i}]") for i in range(12)]
    circuit = QCircuit()
    
    # First rotation layer
    circuit << RY(qubits[0], params[0])
    circuit << RY(qubits[1], params[1])
    circuit << RY(qubits[2], params[2])
    circuit << RZ(qubits[0], params[3])
    circuit << RZ(qubits[1], params[4])
    circuit << RZ(qubits[2], params[5])
    
    # Barrier
    circuit << BARRIER(qubits)
    
    # Entanglement layer (full)
    circuit << CNOT(qubits[0], qubits[1])
    circuit << CNOT(qubits[0], qubits[2])
    circuit << CNOT(qubits[1], qubits[2])
    
    # Barrier
    circuit << BARRIER(qubits)
    
    # Final rotation layer
    circuit << RY(qubits[0], params[6])
    circuit << RY(qubits[1], params[7])
    circuit << RY(qubits[2], params[8])
    circuit << RZ(qubits[0], params[9])
    circuit << RZ(qubits[1], params[10])
    circuit << RZ(qubits[2], params[11])
    
    return circuit
