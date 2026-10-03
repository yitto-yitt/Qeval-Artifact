# EVAL_META: task_id=27, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def apply_op_back():
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    # In pyQPanda, we work directly with programs and gates
    # We'll add another H gate to qubit 0 at the end
    prog << pq.H(qubits[0])
    
    return prog

result = apply_op_back()
machine.finalize()
