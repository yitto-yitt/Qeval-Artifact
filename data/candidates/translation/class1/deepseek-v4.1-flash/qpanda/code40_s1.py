# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, amplitude_encode, measure

def init_random_3qubit(desired_vector):
    n = 3
    # Normalize the desired vector (as Qiskit's initialize does)
    norm = sum(abs(x)**2 for x in desired_vector) ** 0.5
    normalized = [x / norm for x in desired_vector]
    
    # Convert from Qiskit little-endian to QPanda big-endian by reversing the bits of the index
    reversed_vector = [0j] * (2**n)
    for i in range(2**n):
        rev = 0
        for b in range(n):
            if (i >> b) & 1:
                rev |= 1 << (n - 1 - b)
        reversed_vector[rev] = normalized[i]
    
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n)
    c = qvm.cAlloc_many(n)
    prog = QProg()
    prog << amplitude_encode(reversed_vector, q)
    for i in range(n):
        prog << measure(q[i], c[i])
    shots = 1024
    result = qvm.run_with_configuration(prog, c, shots)
    total = sum(result.values())
    # Convert QPanda big-endian keys to Qiskit little-endian bitstrings
    return {format(key, '03b')[::-1]: count / total for key, count in result.items()}
