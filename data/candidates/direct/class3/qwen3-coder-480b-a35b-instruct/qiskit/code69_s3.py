# EVAL_META: task_id=69, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QuantumCircuit(2)
    
    # H gate on quantum register 0
    qc.h(0)
    
    # Controlled-S gate on quantum register 0 (control) and 1 (target)
    qc.cp(1.5708, 0, 1)  # S gate is equivalent to CP(pi/2)
    
    # H gate on quantum register 1
    qc.h(1)
    
    # Controlled-S dagger gate on quantum register 1 (control) and 0 (target)
    qc.cp(-1.5708, 1, 0)  # S† gate is equivalent to CP(-pi/2)
    
    return qc
