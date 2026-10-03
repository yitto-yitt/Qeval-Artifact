# EVAL_META: task_id=84, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *

def controlled_custom_unitary_circuit():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    
    # Define the custom unitary matrix for U3 gate with parameters (0.3, 0.2, 0.1)
    theta = 0.3
    phi = 0.2
    lam = 0.1
    
    # U3 gate matrix: [[cos(theta/2), -exp(i*lam)*sin(theta/2)], 
    #                  [exp(i*phi)*sin(theta/2), exp(i*(phi+lam))*cos(theta/2)]]
    cos_val = complex(cos(theta/2), 0)
    sin_val = complex(-sin(theta/2), 0) * complex(cos(lam), sin(lam))
    third_val = complex(sin(theta/2), 0) * complex(cos(phi), sin(phi))
    fourth_val = complex(cos(theta/2), 0) * complex(cos(phi+lam), sin(phi+lam))
    
    u_matrix = [
        [cos_val, sin_val],
        [third_val, fourth_val]
    ]
    
    # Apply controlled version of the custom unitary gate
    cgate = pq.ControlledQGate(pq.U(u_matrix[0][0], u_matrix[0][1], u_matrix[1][0], u_matrix[1][1]), [qubits[0]])
    prog.insert(cgate(qubits[1]))
    
    pq.destroy_quantum_machine(machine)
    return prog
