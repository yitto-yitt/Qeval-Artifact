# EVAL_META: task_id=105, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
qubits = machine.qAlloc_many(2)

def initialize_cnot_dihedral():
    prog = pq.QProg()
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.T(qubits[0]))
    
    # In pyQPanda, we don't have direct CNOTDihedral equivalent
    # We return the program which represents the circuit
    return prog

machine.finalize()
