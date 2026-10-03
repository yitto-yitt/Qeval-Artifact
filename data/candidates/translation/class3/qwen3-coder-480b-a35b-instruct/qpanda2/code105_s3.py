# EVAL_META: task_id=105, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def initialize_cnot_dihedral():
    prog = pq.QProg()
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.T(qubits[0]))
    
    # In pyqpanda, we don't have a direct CNOTDihedral equivalent
    # We'll return the program as the closest representation
    return prog

machine.finalize()
