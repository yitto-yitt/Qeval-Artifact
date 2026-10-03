# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    if hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
    elif hasattr(oracle, 'num_wires'):
        n = oracle.num_wires
    elif hasattr(oracle, 'wires'):
        n = len(oracle.wires)
    else:
        raise ValueError("Cannot determine number of wires from oracle")

    all_wires = list(range(n))
    input_wires = list(range(n - 1))
    output_wire = n - 1

    dev = qml.device('default.qubit', wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=output_wire)
        for w in all_wires:
            qml.Hadamard(wires=w)

        if callable(oracle):
            oracle(all_wires)
        else:
            qml.apply(oracle)

        for w in all_wires:
            qml.Hadamard(wires=w)

        return qml.probs(wires=input_wires)

    probs = circuit()

    dist = {}
    for idx, prob in enumerate(probs):
        if prob > 1e-10:
            bitstring = format(idx, f'0{n-1}b')[::-1]
            dist[bitstring] = float(prob)
    return dist
