# EVAL_META: task_id=90, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_custom_controlled():
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(4)
    
    prog = pq.QProg()
    
    # Create the custom gate: X on qubit 0, H on qubit 1
    custom_prog = pq.QProg()
    custom_prog << pq.X(qubits[0]) << pq.H(qubits[1])
    
    # Create controlled version with 2 control qubits
    controlled_gate = pq.add_control_qgate(custom_prog, [qubits[0], qubits[3]])
    
    # Apply to the main circuit: controls on qubits 0 and 3, targets on qubits 1 and 2
    prog << controlled_gate
    
    return prog
