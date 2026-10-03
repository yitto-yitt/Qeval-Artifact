# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    # Convert desired_vector to a list of complex numbers
    state_vector = [complex(x) for x in desired_vector]
    encode_circuit = pq.amplitude_encode(qubits, state_vector)
    prog.insert(encode_circuit)
    
    # Measure qubits
    for i in range(3):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
        
    try:
        machine.set_random_seed(42)
    except AttributeError:
        pass
        
    shots = 1024
    result = machine.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(result.values())
    
    # Qiskit's bitstring has qubit 0 as the rightmost bit (LSB).
    # pyqpanda's run_with_configuration returns keys where the first cbit in the list is the leftmost bit (MSB).
    # We reverse the keys to match Qiskit's bit ordering.
    prob_dist = {key[::-1]: val / total for key, val in result.items()}
    
    machine.finalize()
    return prob_dist
