# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def create_efficientSU2():
    # In pyQPanda, we need to manually construct the EfficientSU2-like circuit
    # since there's no direct equivalent to Qiskit's EfficientSU2
    prog = pq.QProg()
    
    # Apply initial rotation gates (RY and RZ) on all qubits
    for i in range(3):
        prog << pq.RY(qubits[i], pq.Parameter("theta_{}".format(i*2)))
        prog << pq.RZ(qubits[i], pq.Parameter("theta_{}".format(i*2+1)))
    
    # Add entangling layer - CNOTs between adjacent qubits
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.CNOT(qubits[1], qubits[2])
    
    # Add another layer of rotation gates
    for i in range(3):
        prog << pq.RY(qubits[i], pq.Parameter("theta_{}".format(6+i*2)))
        prog << pq.RZ(qubits[i], pq.Parameter("theta_{}".format(6+i*2+1)))
    
    return prog

machine.finalize()
