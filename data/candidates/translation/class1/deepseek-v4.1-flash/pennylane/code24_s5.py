# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import inspect

def dj_algorithm(oracle):
    # Determine number of wires and how to apply the oracle
    if hasattr(oracle, 'device'):
        n = len(oracle.device.wires)
        def apply_oracle(wires):
            oracle.func(wires=wires)
    elif hasattr(oracle, 'num_wires'):
        n = oracle.num_wires
        def apply_oracle(wires):
            oracle(wires=wires)
    elif hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
        def apply_oracle(wires):
            oracle(wires=wires)
    else:
        # Fallback: try to infer n from function signature or closure
        n = None
        if callable(oracle):
            sig = inspect.signature(oracle)
            for param in sig.parameters.values():
                if param.name in ['n', 'num_wires', 'num_qubits'] and param.default is not inspect.Parameter.empty:
                    n = param.default
                    break
            if n is None and hasattr(oracle, '__closure__') and oracle.__closure__:
                for cell in oracle.__closure__:
                    try:
                        val = cell.cell_contents
                        if isinstance(val, int) and val > 0:
                            n = val
                            break
                    except:
                        pass
        if n is None:
            raise ValueError("Cannot determine number of wires from oracle")
        def apply_oracle(wires):
            oracle(wires=wires)

    if n == 1:
        return {'': 1.0}

    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for i in range(n):
            qml.Hadamard(wires=i)
        apply_oracle(wires=range(n))
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.probs(wires=range(n-1))

    probs = circuit()
    result = {}
    for i, p in enumerate(probs):
        bitstring = format(i, f'0{n-1}b')[::-1]
        result[bitstring] = p
    return result
