# EVAL_META: task_id=89, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_controlled_hgate():
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(3)
    
    prog = pq.QProg()
    ctrl_qubits = [qubits[0], qubits[1]]
    target_qubit = qubits[2]
    
    # Create controlled Hadamard gate using two control qubits
    prog.insert(pq.H(target_qubit).control(ctrl_qubits))
    
    return prog
