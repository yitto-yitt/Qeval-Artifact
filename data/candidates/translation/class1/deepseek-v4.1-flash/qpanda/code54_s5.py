# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, Toffoli, Measure

def and_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(9)
    c = qvm.cAlloc_many(3)
    a_qubits = q[0:3]
    b_qubits = q[3:6]
    anc_qubits = q[6:9]
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    prog = QProg()
    for i in range(3):
        if a_bin[2 - i] == '1':
            prog << X(a_qubits[i])
        if b_bin[2 - i] == '1':
            prog << X(b_qubits[i])
    
    for i in range(3):
        prog << Toffoli(a_qubits[i], b_qubits[i], anc_qubits[i])
    
    # Reverse mapping to match Qiskit's MSB-left bitstring ordering
    prog << Measure(anc_qubits[2], c[0])
    prog << Measure(anc_qubits[1], c[1])
    prog << Measure(anc_qubits[0], c[2])
    
    result = qvm.run_with_configuration(prog, c, 1024)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
