# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    # Convert desired_vector to a list of complex numbers
    vector_list = [complex(x) for x in desired_vector]
    
    # Encode the amplitude into the qubits
    circuit = pq.amplitude_encode(q, vector_list)
    prog.insert(circuit)
    
    # Measure all qubits
    for i in range(3):
        prog.insert(pq.Measure(q[i], c[i]))
        
    # Run the program on the simulator
    shots = 10000
    result = machine.run_with_configuration(prog, c, shots)
    
    # Calculate the probability distribution
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
