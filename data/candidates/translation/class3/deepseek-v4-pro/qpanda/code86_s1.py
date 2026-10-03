# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import (
    QProg, H, CNOT, TransforFactory,
    init_quantum_machine, finalize_quantum_machine
)

def collect_linear_blocks_with_and_without_limit():
    qvm = init_quantum_machine()
    qubits = qvm.qAlloc_many(5)
    prog = QProg()
    prog << H(qubits[0]) \
         << CNOT(qubits[0], qubits[1]) \
         << CNOT(qubits[1], qubits[2]) \
         << CNOT(qubits[2], qubits[3]) \
         << CNOT(qubits[3], qubits[4])
    
    # No block width restriction
    collect_full = TransforFactory.createLinearFunctionsCollector()
    full_prog = collect_full.execute(prog)
    
    # With max_block_width = 3
    collect_limited = TransforFactory.createLinearFunctionsCollector(max_block_width=3)
    limited_prog = collect_limited.execute(prog)
    
    finalize_quantum_machine(qvm)
    return full_prog, limited_prog
