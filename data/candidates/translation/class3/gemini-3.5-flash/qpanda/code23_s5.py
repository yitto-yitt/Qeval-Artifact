# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, qAlloc_many, init_quantum_machine

def dj_constant_oracle():
    try:
        qubits = qAlloc_many(3)
    except Exception:
        init_quantum_machine(0)
        qubits = qAlloc_many(3)
    
    circuit = QCircuit()
    circuit << X(qubits[2])
    return circuit
