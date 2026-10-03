# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np


def dj_algorithm(oracle):
    def _num_qubits(obj):
        num = getattr(obj, "num_qubits", None)
        if num is not None:
            return int(num() if callable(num) else num)
        if hasattr(obj, "qubits"):
            return len(obj.qubits)
        if hasattr(obj, "all_qubits"):
            return len(obj.all_qubits())
        raise ValueError("Cannot determine oracle qubit count.")

    def _oracle_qubits(obj):
        if isinstance(obj, cirq.Operation):
            return list(obj.qubits)
        if hasattr(obj, "all_qubits"):
            qs = list(cirq.QubitOrder.DEFAULT.order_for(obj.all_qubits()))
            if qs:
                return qs
        return list(cirq.LineQubit.range(_num_qubits(obj)))

    qubits = _oracle_qubits(oracle)
    n = len(qubits)
    output_qubit = qubits[-1]
    input_qubits = qubits[:-1]

    circuit = cirq.Circuit()
    circuit.append(cirq.X(output_qubit))
    circuit.append(cirq.H.on_each(*qubits))

    if isinstance(oracle, cirq.Gate):
        circuit.append(oracle.on(*qubits))
    elif callable(oracle) and not isinstance(oracle, cirq.Operation):
        try:
            circuit.append(oracle(*qubits))
        except TypeError:
            circuit.append(oracle(qubits))
    else:
        circuit.append(oracle)

    circuit.append(cirq.H.on_each(*qubits))

    result = cirq.Simulator(dtype=np.complex128).simulate(circuit, qubit_order=qubits)
    state = result.final_state_vector

    probs = {}
    for i, amp in enumerate(state):
        p = float(abs(amp) ** 2)
        if p <= 1e-12:
            continue
        bits = format(i, f"0{n}b")
        key = bits[: len(input_qubits)][::-1]
        probs[key] = probs.get(key, 0.0) + p

    probs = {k: v for k, v in probs.items() if v > 1e-12}
    total = sum(probs.values())
    return {k: v / total for k, v in probs.items()}
