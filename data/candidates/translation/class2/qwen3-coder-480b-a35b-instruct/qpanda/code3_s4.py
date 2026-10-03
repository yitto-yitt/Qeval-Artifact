# EVAL_META: task_id=3, framework=qpanda, class=2
import pyqpanda3 as pq


def create_ghz(drawing=False):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.CNOT(qubits[0], qubits[2]))
    
    for i in range(3):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    
    if drawing:
        # pyqpanda3 doesn't have built-in drawing capabilities like Qiskit
        # Return the program and None for drawing
        return prog, None
    return prog
