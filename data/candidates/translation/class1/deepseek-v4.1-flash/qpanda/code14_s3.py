# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure

def bell_each_shot():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])

    result = qvm.run_with_shots(prog, 10)
    counts = result.get_counts() if hasattr(result, 'get_counts') else result

    normalized = {}
    for k, v in counts.items():
        if isinstance(k, int):
            key = format(k, '02b')
        elif isinstance(k, str):
            if all(c in '01' for c in k):
                key = k.zfill(2)
            else:
                key = format(int(k), '02b')
        else:
            key = str(k)
        normalized[key] = normalized.get(key, 0) + v

    total = sum(normalized.values())
    return {k: v / total for k, v in normalized.items()}
