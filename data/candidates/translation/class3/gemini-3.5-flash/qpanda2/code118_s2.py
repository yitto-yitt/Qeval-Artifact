# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)
c = machine.cAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    control_qubits = pq.QVec()
    control_qubits.append(q[0])
    control_qubits.append(q[1])
    control_qubits.append(q[2])
    
    gate = pq.SX(q[3]).control(control_qubits)
    prog.insert(gate)
    return prog

machine.finalize()
