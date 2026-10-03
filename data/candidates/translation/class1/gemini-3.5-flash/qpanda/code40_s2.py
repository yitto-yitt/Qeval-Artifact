# EVAL_META: task_id=40, framework=qpanda, class=1
import pyqpanda3.core as pq
import math

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    if hasattr(desired_vector, 'tolist'):
        state_list = desired_vector.tolist()
    else:
        state_list = list(desired_vector)
        
    state_list = [complex(x) for x in state_list]
    
    # Normalize the state vector to be safe
    norm = math.sqrt(sum(abs(x)**2 for x in state_list))
    if norm > 0:
        state_list = [x / norm for x in state_list]
        
    circuit = pq.amplitude_encode(qubits, state_list)
    
    prog = pq.QProg()
    prog << circuit
    
    for i in range(3):
        prog << pq.Measure(qubits[i], cbits[i])
        
    shots = 10000
    result = machine.run_with_configuration(prog, cbits, shots)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
