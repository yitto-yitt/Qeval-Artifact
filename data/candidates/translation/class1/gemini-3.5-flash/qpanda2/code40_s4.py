# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    if hasattr(desired_vector, 'tolist'):
        desired_vector = desired_vector.tolist()
    else:
        desired_vector = list(desired_vector)
        
    desired_vector = [complex(x) for x in desired_vector]
    
    encode_circuit = pq.amplitude_encode(qubits, desired_vector)
    
    prog = pq.QProg()
    prog << encode_circuit
    
    for i in range(3):
        prog << pq.MEASURE(qubits[i], cbits[i])
        
    shots = 1000
    result = machine.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
