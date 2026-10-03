# EVAL_META: task_id=86, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.CNOT(qubits[1], qubits[2])
    prog << pq.CNOT(qubits[2], qubits[3])
    prog << pq.CNOT(qubits[3], qubits[4])
    
    # pyQPanda does not have a direct equivalent to Qiskit's CollectLinearFunctions transpiler pass.
    # We return the constructed quantum program for both cases.
    return prog, prog

machine.finalize()
