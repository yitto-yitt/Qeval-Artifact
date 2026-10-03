# EVAL_META: task_id=84, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    prog = pq.QProg()
    
    # Define the custom 1-qubit unitary gate with angles 0.3, 0.2, 0.1
    # In pyQPanda, U3 gate is represented as U(θ, φ, λ)
    prog << pq.U(qubits[1], 0.3, 0.2, 0.1) * pq.CTRL(qubits[0])
    
    return prog

machine.finalize()
