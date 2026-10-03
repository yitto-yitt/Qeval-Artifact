# EVAL_META: task_id=24, framework=pennylane, class=1
import numpy as np
import pennylane as qml
import inspect

def dj_algorithm(oracle):
    if hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
    elif hasattr(oracle, 'num_wires'):
        n = oracle.num_wires
    elif hasattr(oracle, 'wires'):
        n = len(oracle.wires)
    elif hasattr(oracle, 'shape'):
        n = int(np.round(np.log2(oracle.shape[0])))
    else:
        n = oracle.num_qubits

    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for i in range(n):
            qml.Hadamard(wires=i)
            
        if isinstance(oracle, qml.operation.Operation):
            qml.apply(oracle)
        elif isinstance(oracle, qml.tape.QuantumTape):
            for op in oracle.operations:
                qml.apply(op)
        elif callable(oracle):
            try:
                sig = inspect.signature(oracle)
                if len(sig.parameters) > 0:
                    oracle(wires=range(n))
                else:
                    oracle()
            except Exception:
                oracle()
        elif hasattr(oracle, 'shape'):
            qml.QubitUnitary(np.array(oracle), wires=range(n))
        else:
            try:
                qml.from_qiskit(oracle)()
            except Exception:
                pass
            
        for i in range(n):
            qml.Hadamard(wires=i)
            
        return qml.probs(wires=range(n - 1))

    probs = circuit()
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-9:
            bitstring = format(i, f'0{n-1}b')[::-1]
            result[bitstring] = float(p)
            
    return result
