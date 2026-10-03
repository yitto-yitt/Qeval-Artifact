# EVAL_META: task_id=24, framework=pennylane, class=1
import inspect
import pennylane as qml

def dj_algorithm(oracle):
    if hasattr(oracle, "num_wires"):
        n = oracle.num_wires
    elif hasattr(oracle, "wires"):
        n = len(oracle.wires)
    elif hasattr(oracle, "num_qubits"):
        n = oracle.num_qubits
    else:
        raise ValueError("Cannot determine number of wires from oracle")

    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for i in range(n):
            qml.Hadamard(wires=i)

        if isinstance(oracle, qml.QNode):
            for op in oracle.tape.operations:
                qml.apply(op)
        elif hasattr(oracle, "operations"):
            for op in oracle.operations:
                qml.apply(op)
        else:
            try:
                sig = inspect.signature(oracle)
            except (TypeError, ValueError):
                oracle(wires=list(range(n)))
            else:
                if "wires" in sig.parameters:
                    oracle(wires=list(range(n)))
                else:
                    oracle()

        for i in range(n):
            qml.Hadamard(wires=i)

        return qml.probs(wires=range(n - 1))

    probs = circuit()
    return {format(i, f"0{n - 1}b"): float(probs[i]) for i in range(len(probs)) if probs[i] > 0}
