# EVAL_META: task_id=44, framework=qiskit, class=3
from qiskit import QuantumCircuit

def tensor_circuits():
    qc_cry = QuantumCircuit(2)
    qc_cry.cry(0.2, 0, 1)
    
    qc_x = QuantumCircuit(1)
    qc_x.x(0)
    
    return qc_cry.tensor(qc_x)
