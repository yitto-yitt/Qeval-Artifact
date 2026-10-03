# EVAL_META: task_id=84, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3.core import *

def controlled_custom_unitary_circuit():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    
    # Define custom unitary matrix for U3 gate with parameters (0.3, 0.2, 0.1)
    theta = 0.3
    phi = 0.2
    lam = 0.1
    
    # U3 gate matrix: [[cos(theta/2), -exp(i*lam)*sin(theta/2)], 
    #                  [exp(i*phi)*sin(theta/2), exp(i*(phi+lam))*cos(theta/2)]]
    cos_val = complex(cos(theta/2), 0)
    sin_val = complex(-sin(theta/2) * cos(lam), -sin(theta/2) * sin(lam))  # -exp(i*lam)*sin(theta/2)
    sin_val2 = complex(sin(theta/2) * cos(phi), sin(theta/2) * sin(phi))   # exp(i*phi)*sin(theta/2)
    cos_val2 = complex(cos(theta/2) * cos(phi + lam), cos(theta/2) * sin(phi + lam))  # exp(i*(phi+lam))*cos(theta/2)
    
    u_matrix = [[cos_val, sin_val], [sin_val2, cos_val2]]
    
    # Create controlled version of the custom unitary gate
    ctrl_qubit = qubits[0]
    target_qubit = qubits[1]
    
    # Apply the controlled custom unitary gate
    prog.insert(pq.RX(target_qubit, theta/2))
    prog.insert(pq.RZ(target_qubit, lam))
    prog.insert(pq.RX(target_qubit, theta/2))
    prog.insert(pq.RZ(target_qubit, phi))
    prog.insert(pq.CU(prog, ctrl_qubit, target_qubit, theta, phi, lam, 0))
    
    # Actually, let's use the proper controlled unitary approach
    prog = pq.QProg()
    prog.insert(pq.U3(qubits[1], theta, phi, lam).control(ctrl_qubit))
    
    pq.destroy_quantum_machine(machine)
    return prog
