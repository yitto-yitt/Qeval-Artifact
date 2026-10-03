# EVAL_META: task_id=67, framework=qpanda2, class=1
import pyqpanda as pq
from numpy import pi


def chsh_circuit(alice, bob):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.Barrier(qubits))
    
    if alice == 0:
        prog.insert(pq.RY(0, qubits[0]))
    else:
        prog.insert(pq.RY(-pi / 2, qubits[0]))
        
    prog.insert(pq.Measure(qubits[0], cbits[0]))
    
    if bob == 0:
        prog.insert(pq.RY(-pi / 4, qubits[1]))
    else:
        prog.insert(pq.RY(pi / 4, qubits[1]))
        
    prog.insert(pq.Measure(qubits[1], cbits[1]))
    
    # Since pyQPanda doesn't have a direct circuit object like Qiskit,
    # we return the program which represents the quantum circuit
    return prog
