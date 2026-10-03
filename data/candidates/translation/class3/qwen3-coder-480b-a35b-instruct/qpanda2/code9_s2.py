# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_efficientSU2():
    prog = pq.QProg()
    
    # Create EfficientSU2-like circuit manually since pyQPanda doesn't have direct equivalent
    # EfficientSU2 consists of alternating rotation layers and entanglement layers
    
    # First rotation layer (RY gates)
    for i in range(3):
        prog << pq.RY(qubits[i], pq.Parameter("theta_{}".format(i)))
    
    # Entanglement layer (CNOTs in linear topology)
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.CNOT(qubits[1], qubits[2])
    
    # Second rotation layer (RY gates)
    for i in range(3):
        prog << pq.RY(qubits[3 + i], pq.Parameter("theta_{}".format(i + 3)))
    
    # Add barrier
    prog << pq.BARRIER()
    
    return prog

result = create_efficientSU2()
machine.finalize()
