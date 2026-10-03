# EVAL_META: task_id=26, framework=qpanda2, class=3
import pyqpanda as pq


machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def bell_dag():
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    
    # In pyQPanda, we don't have a direct equivalent to Qiskit's DAG
    # We return the quantum program as the closest equivalent
    return prog


machine.finalize()
