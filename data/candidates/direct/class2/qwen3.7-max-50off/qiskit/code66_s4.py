# EVAL_META: task_id=66, framework=qiskit, class=2
import math
from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3, 3)
    
    # Create superposition on q0: sqrt(2/3)|0> + sqrt(1/3)|1>
    theta = 2 * math.asin(1 / math.sqrt(3))
    qc.ry(theta, 0)
    
    # Apply Hadamard on q1 controlled by q0 being |1>
    # Since we want to split the |0> component of q0, we flip q0 first
    qc.x(0)
    qc.ch(0, 1)
    qc.x(0)
    
    # Now the state is 1/sqrt(3) (|000> + |010> + |100>)
    # We need to flip q2 when q0=0 and q1=0 to change |000> to |001>
    qc.x(0)
    qc.x(1)
    qc.ccx(0, 1, 2)
    qc.x(0)
    qc.x(1)
    
    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])
    
    return qc
