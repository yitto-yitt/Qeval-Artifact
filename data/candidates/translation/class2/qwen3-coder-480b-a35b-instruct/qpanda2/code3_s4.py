# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


def create_ghz(drawing=False):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    prog = pq.QProg()
    
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.CNOT(qubits[0], qubits[2]))
    
    # Measure all qubits
    cbits = machine.cAlloc_many(3)
    for i in range(3):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    
    if drawing:
        # pyQPanda doesn't have built-in drawing like Qiskit
        # Return the program and None for drawing
        return prog, None
    
    machine.finalize()
    return prog
