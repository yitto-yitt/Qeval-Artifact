# EVAL_META: task_id=40, framework=qpanda, class=1
import pyqpanda3.core as pq

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    circuit = pq.amplitude_encode(qubits, desired_vector)
    
    prog = pq.QProg()
    prog.insert(circuit)
    
    for i in range(3):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
        
    result = machine.run_with_configuration(prog, cbits, 1024)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
