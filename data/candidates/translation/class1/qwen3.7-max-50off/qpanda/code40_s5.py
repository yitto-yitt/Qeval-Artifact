# EVAL_META: task_id=40, framework=qpanda, class=1
import pyqpanda3 as pq

def init_random_3qubit(desired_vector):
    if hasattr(desired_vector, 'tolist'):
        desired_vector = desired_vector.tolist()
        
    qvm = pq.QVM()
    qubits = qvm.qAlloc(3)
    prog = pq.QProg()
    prog << pq.init_state(qubits, desired_vector)
    
    cbits = qvm.cAlloc(3)
    for i in range(3):
        prog << pq.Measure(qubits[i], cbits[i])
        
    result = qvm.run_with_configuration(prog, cbits, 1000)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
