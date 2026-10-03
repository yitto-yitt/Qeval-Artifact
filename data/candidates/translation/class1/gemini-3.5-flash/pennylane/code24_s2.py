# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    # Determine the number of qubits and how to call the oracle
    if hasattr(oracle, "num_qubits"):
        n = oracle.num_qubits
        wires = list(range(n))
        oracle_fn = lambda: qml.from_qiskit(oracle)(wires=wires)
    elif hasattr(oracle, "wires") and oracle.wires:
        wires = list(oracle.wires)
        n = len(wires)
        oracle_fn = lambda: qml.apply(oracle)
    elif callable(oracle):
        tape = qml.tape.make_tape(oracle)()
        wires = list(tape.wires)
        n = len(wires)
        oracle_fn = oracle
    else:
        raise ValueError("Unsupported oracle type")

    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        # Prepare state |+>^{\otimes n-1} |->
        qml.PauliX(wires=n - 1)
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Apply oracle
        oracle_fn()
        
        # Apply H to input register
        for i in range(n - 1):
            qml.Hadamard(wires=i)
            
        return qml.probs(wires=range(n - 1))

    probs = circuit()
    num_input_qubits = n - 1
    
    result = {}
    for i, p in enumerate(probs):
        # Qiskit uses little-endian (qubit 0 is rightmost), so we reverse the big-endian bitstring
        bitstring = format(i, f'0{num_input_qubits}b')[::-1]
        result[bitstring] = float(p)
        
    return result
