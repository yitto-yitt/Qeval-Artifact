# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_efficientSU2():
    circuit = QCircuit()
    params = [var(f"theta[{i}]") for i in range(12)]
    idx = 0
    
    circuit << BARRIER(qubits)
    
    for q in qubits:
        circuit << RY(q, params[idx]); idx += 1
        circuit << RZ(q, params[idx]); idx += 1
    
    circuit << BARRIER(qubits)
    
    circuit << CNOT(qubits[0], qubits[1])
    circuit << CNOT(qubits[0], qubits[2])
    circuit << CNOT(qubits[1], qubits[2])
    
    circuit << BARRIER(qubits)
    
    for q in qubits:
        circuit << RY(q, params[idx]); idx += 1
        circuit << RZ(q, params[idx]); idx += 1
    
    circuit << BARRIER(qubits)
    
    return circuit

machine.finalize()
