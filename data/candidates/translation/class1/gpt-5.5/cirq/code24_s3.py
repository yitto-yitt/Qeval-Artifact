# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    qset = set()
    if hasattr(oracle, "all_qubits"):
        qset = set(oracle.all_qubits())
    elif hasattr(oracle, "qubits"):
        qset = set(oracle.qubits)
    else:
        try:
            qset = {q for op in cirq.flatten_to_ops(oracle) for q in op.qubits}
        except Exception:
            qset = set()

    n_attr = None
    if hasattr(oracle, "num_qubits"):
        nq = getattr(oracle, "num_qubits")
        try:
            n_attr = int(nq() if callable(nq) else nq)
        except Exception:
            n_attr = None

    if n_attr is not None and (not qset):
        qubits = list(cirq.LineQubit.range(n_attr))
    elif n_attr is not None and len(qset) < n_attr and all(isinstance(q, cirq.LineQubit) for q in qset):
        qubits = list(cirq.LineQubit.range(n_attr))
    else:
        qubits = list(cirq.QubitOrder.DEFAULT.order_for(qset))

    n = len(qubits)
    output_qubit = qubits[-1]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append(cirq.H.on_each(*qubits))

    if isinstance(oracle, cirq.Gate):
        circuit.append(oracle.on(*qubits))
    elif isinstance(oracle, cirq.Operation):
        circuit.append(oracle)
    else:
        circuit.append(oracle)

    circuit.append(cirq.H.on_each(*qubits))

    result = cirq.Simulator().simulate(circuit, qubit_order=qubits)
    state = result.final_state_vector

    probs = {}
    for idx, amp in enumerate(state):
        p = float(np.abs(amp) ** 2)
        if p > 1e-12:
            bits = [(idx >> (n - 1 - i)) & 1 for i in range(n)]
            key = "".join(str(bits[i]) for i in range(n - 2, -1, -1))
            probs[key] = probs.get(key, 0.0) + p

    total = sum(probs.values())
    return {key: value / total for key, value in probs.items()}
