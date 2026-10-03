# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
import numpy as np
import atexit
from pyqpanda import *

# Global QVM initialization
qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(10)

# Register cleanup
atexit.register(qvm.finalize)

def to_prog(circuit):
    if isinstance(circuit, QProg):
        return circuit
    prog = QProg()
    prog.insert(circuit)
    return prog

def equivalent_clifford_circuit(circuit, n):
    prog = to_prog(circuit)
    try:
        u = get_unitary_of_qprog(prog)
        num_qubits = int(np.log2(np.sqrt(len(u))))
    except Exception:
        num_qubits = 10
        
    qc_list = []
    for _ in range(n):
        new_prog = QProg()
        new_prog.insert(circuit)
        # Append random identity Clifford gates to preserve equivalence
        for _ in range(random.randint(1, 5)):
            gate_type = random.choice(['H', 'S', 'CNOT'])
            if gate_type == 'CNOT' and num_qubits > 1:
                q1, q2 = random.sample(range(num_qubits), 2)
                new_prog.insert(CNOT(qubits[q1], qubits[q2]))
                new_prog.insert(CNOT(qubits[q1], qubits[q2]))
            elif gate_type == 'H':
                q = random.randint(0, num_qubits - 1)
                new_prog.insert(H(qubits[q]))
                new_prog.insert(H(qubits[q]))
            elif gate_type == 'S':
                q = random.randint(0, num_qubits - 1)
                for _ in range(4):
                    new_prog.insert(S(qubits[q]))
        qc_list.append(new_prog)
    return qc_list
