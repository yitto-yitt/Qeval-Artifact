# EVAL_META: task_id=119, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)
def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    circuit = QCircuit()
    if kind == 'half':
        if n >= 1:
            circuit << CNOT(qubits[0], qubits[n])
    elif kind == 'full':
        if n >= 1:
            circuit << CCNOT(qubits[0], qubits[n], qubits[2*n])
            circuit << CNOT(qubits[0], qubits[n])
    else:
        for i in range(n):
            circuit << CNOT(qubits[i], qubits[n+i])
            if i < n-1:
                circuit << CCNOT(qubits[i], qubits[n+i], qubits[2*n])
                circuit << CNOT(qubits[i], qubits[n+i])
    prog = QProg()
    prog << circuit
    machine.directly_run(prog)
    return circuit
machine.finalize()
