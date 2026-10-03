# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    # Determine the number of qubits
    if hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
    elif hasattr(oracle, 'num_wires'):
        n = oracle.num_wires
    elif hasattr(oracle, 'device'):
        n = len(oracle.device.wires)
    elif hasattr(oracle, 'wires'):
        n = len(oracle.wires)
    else:
        if hasattr(oracle, 'n'):
            n = oracle.n
        else:
            raise ValueError("Cannot determine number of wires from oracle")
    
    wires = list(range(n))
    dev = qml.device('default.qubit', wires=n)
    
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for w in wires:
            qml.Hadamard(wires=w)
        
        # Apply the oracle
        if hasattr(oracle, 'func'):
            func = oracle.func
        else:
            func = oracle
        try:
            func(wires)
        except TypeError:
            func()
        
        for w in wires:
            qml.Hadamard(wires=w)
        
        # Measure input qubits in reverse order to match Qiskit's bitstring convention
        input_wires = list(range(n-1))
        input_wires_reversed = input_wires[::-1]
        return qml.probs(wires=input_wires_reversed)
    
    probs = circuit()
    n_inputs = n - 1
    if n_inputs == 0:
        return {'': 1.0}
    return {format(i, f'0{n_inputs}b'): probs[i] for i in range(len(probs))}
