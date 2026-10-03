# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import itertools

def dj_algorithm(oracle):
    # Determine the wires and number of qubits
    if hasattr(oracle, "wires") and oracle.wires:
        wires = list(oracle.wires)
        n = len(wires)
    elif hasattr(oracle, "num_qubits"):
        n = oracle.num_qubits
        wires = list(range(n))
    else:
        # Try to trace to find wires
        try:
            with qml.queuing.AnnotatedQueue() as q:
                if callable(oracle):
                    oracle()
            tape = qml.tape.QuantumScript.from_queue(q)
            wires = list(tape.wires)
            n = len(wires)
        except Exception:
            # Fallback
            n = 2
            wires = list(range(n))

    dev = qml.device("default.qubit", wires=wires)

    @qml.qnode(dev)
    def circuit():
        # Step 1: Flip the state of the target qubit (last qubit)
        qml.PauliX(wires=wires[-1])
        
        # Step 2: Apply Hadamard to all qubits
        for w in wires:
            qml.Hadamard(wires=w)
            
        # Step 3: Apply oracle
        if hasattr(oracle, "operations"):
            for op in oracle.operations:
                qml.apply(op)
        elif callable(oracle) and not isinstance(oracle, qml.operation.Operator):
            import inspect
            sig = inspect.signature(oracle)
            if len(sig.parameters) > 0:
                oracle(wires)
            else:
                oracle()
        else:
            qml.apply(oracle)
            
        # Step 4: Apply Hadamard to input qubits
        for w in wires[:-1]:
            qml.Hadamard(wires=w)
            
        # Step 5: Measure the input qubits
        return qml.probs(wires=wires[:-1])

    probs = circuit()
    
    # Format the output as a dictionary of bitstrings
    num_input_qubits = n - 1
    bitstrings = ["".join(x) for x in itertools.product(["0", "1"], repeat=num_input_qubits)]
    probs_list = [float(p) for p in probs]
    
    return dict(zip(bitstrings, probs_list))
