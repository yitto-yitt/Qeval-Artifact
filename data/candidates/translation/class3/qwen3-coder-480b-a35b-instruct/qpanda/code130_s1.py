# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda import *

def inv_circuit(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    cbits = qvm.cAlloc_many(n)
    
    prog = QProg()
    prog.insert(H(qubits[1]))
    prog.insert(H(qubits[2]))
    prog.insert(CNOT(qubits[1], qubits[3]))
    prog.insert(CNOT(qubits[2], qubits[4]))
    
    # Inverse by reversing the circuit
    inverse_prog = QProg()
    for i in range(prog.get_current_node().get_node_type(), 0, -1):
        inverse_prog.insert(prog.get_last_node())
        prog.delete_last_node()
        
    return inverse_prog

    qvm.finalize()
