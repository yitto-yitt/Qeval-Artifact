# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    if hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
        is_qiskit = True
    elif hasattr(oracle, 'num_wires'):
        n = oracle.num_wires
        is_qiskit = False
    else:
        raise ValueError("Oracle must have num_qubits or num_wires attribute.")

    wires = list(range(n))
    meas_wires = list(range(n - 1))[::-1]

    @qml.qnode(qml.device('default.qubit', wires=n))
    def circuit():
        qml.PauliX(wires=n - 1)
        for i in range(n):
            qml.Hadamard(wires=i)
            
        if is_qiskit:
            qml.from_qiskit(oracle)(wires=wires)
        else:
            oracle(wires=wires)
            
        for i in range(n):
            qml.Hadamard(wires=i)
            
        return qml.probs(wires=meas_wires)

    probs = circuit()
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-9:
            bitstring = format(i, f'0{n-1}b')
            result[bitstring] = float(p)
    return result
