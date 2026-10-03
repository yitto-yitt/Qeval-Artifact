# EVAL_META: task_id=89, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_controlled_hgate():
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(3)
    
    prog = pq.QProg()
    # Create a controlled-H gate with 2 control qubits (qubits 0 and 1) and 1 target qubit (qubit 2)
    controlled_h = pq.H(qubits[2])
    controlled_h = pq.ControlledQGate(controlled_h, [qubits[0], qubits[1]])
    prog.insert(controlled_h)
    
    return prog, machine
