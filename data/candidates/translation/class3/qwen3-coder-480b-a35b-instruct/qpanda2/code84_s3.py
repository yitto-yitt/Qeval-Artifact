# EVAL_META: task_id=84, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    prog = pq.QProg()
    
    # Define custom 1-qubit unitary gate with angles 0.3, 0.2, 0.1
    # Using U3 gate: U3(theta, phi, lambda) = U3(0.3, 0.2, 0.1)
    theta = 0.3
    phi = 0.2
    lam = 0.1
    
    # Apply controlled version of the custom unitary gate
    # Control qubit is qubits[0], target qubit is qubits[1]
    prog << pq.U3(qubits[1], theta, phi, lam).c(qubits[0])
    
    return prog

machine.finalize()
