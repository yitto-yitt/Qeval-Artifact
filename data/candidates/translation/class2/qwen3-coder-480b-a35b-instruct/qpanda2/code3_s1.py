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
    prog.insert(pq.Measure(qubits[0], cbits[0]))
    prog.insert(pq.Measure(qubits[1], cbits[1]))
    prog.insert(pq.Measure(qubits[2], cbits[2]))
    
    if drawing:
        # pyQPanda doesn't have a direct drawing method like Qiskit
        # We return the program and None for the drawing
        return prog, None
    
    machine.finalize()
    return prog
