# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    prog = pq.QProg()
    
    # Create controlled RY gate (CRY) with angle 0.2, control q0, target q1
    ctrl_qubits = pq.QVec()
    ctrl_qubits.append(qubits[0])
    cry = pq.RY(qubits[1], 0.2).control(ctrl_qubits)
    
    prog << cry
    prog << pq.X(qubits[2])
    
    return prog

machine.finalize()
