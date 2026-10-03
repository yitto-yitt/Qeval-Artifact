# EVAL_META: task_id=89, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_controlled_hgate():
    prog = pq.QProg()
    ctrl_qubits = [qubits[0], qubits[1]]
    target_qubit = qubits[2]
    
    # Create a controlled-H gate using two control qubits
    prog.insert(pq.H(target_qubit).control(ctrl_qubits))
    
    return prog

machine.finalize()
