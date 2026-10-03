# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QProg, H, X, Measure, CPUQVM

def dj_algorithm(oracle):
    # Extract qubits from the oracle
    if hasattr(oracle, 'get_qubits'):
        qubits = oracle.get_qubits()
    elif hasattr(oracle, 'qubits'):
        qubits = oracle.qubits()
    else:
        # Fallback for callable oracle with num_qubits
        if hasattr(oracle, 'num_qubits') and callable(oracle):
            n = oracle.num_qubits
            qvm = CPUQVM()
            qvm.init_qvm()
            qubits = qvm.qAlloc_many(n)
            prog = QProg()
            prog << oracle(qubits)
            raise NotImplementedError
        else:
            raise ValueError("Cannot extract qubits from oracle")

    # Sort qubits by index to ensure the last one is the output qubit
    qubits = sorted(qubits, key=lambda q: q.get_index())
    n = len(qubits)
    if n == 0:
        return {}

    # Get the QVM instance from a qubit
    q0 = qubits[0]
    if hasattr(q0, 'get_qvm'):
        qvm = q0.get_qvm()
    elif hasattr(q0, 'qvm'):
        qvm = q0.qvm()
    else:
        raise RuntimeError("Cannot get QVM from qubit")

    # Build the Deutsch-Jozsa circuit
    prog = QProg()
    prog << X(qubits[n-1])
    for i in range(n):
        prog << H(qubits[i])
    prog << oracle
    for i in range(n-1):
        prog << H(qubits[i])

    # Measure the input register (first n-1 qubits)
    # Reverse the qubit order to match Qiskit's bitstring convention
    input_qubits = qubits[:n-1][::-1]
    if hasattr(qvm, 'prob_run'):
        result = qvm.prob_run(prog, input_qubits, -1)
    else:
        cbits = qvm.cAlloc_many(n-1)
        for i in range(n-1):
            prog << Measure(qubits[i], cbits[i])
        shots = 4096
        counts = qvm.run_with_configuration(prog, cbits, shots)
        total = sum(counts.values())
        result = {k: v / total for k, v in counts.items()}

    return result
