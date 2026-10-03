# EVAL_META: task_id=109, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def circuit():
    qubits = machine.qAlloc_many(1)
    prog = pq.QProg()
    
    # Apply H gate
    prog.insert(pq.H(qubits[0]))
    
    # Define parameter theta
    theta = pq.Parameter("th")
    
    # Apply RZ gate with parameter
    prog.insert(pq.RZ(qubits[0], theta))
    
    return prog, qubits, theta

machine.finalize()
