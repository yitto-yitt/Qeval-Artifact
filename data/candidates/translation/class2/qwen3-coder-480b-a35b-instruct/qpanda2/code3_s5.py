# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


def create_ghz(drawing=False):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.CNOT(qubits[0], qubits[2]))
    
    for i in range(3):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    
    if drawing:
        # pyQPanda doesn't have a direct draw method like Qiskit
        # We return the program and a string representation instead
        return prog, str(prog)
    return prog
