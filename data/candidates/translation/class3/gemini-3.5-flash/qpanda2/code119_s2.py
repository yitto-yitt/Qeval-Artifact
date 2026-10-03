# EVAL_META: task_id=119, framework=qpanda2, class=3
from pyqpanda import *

# Initialize global QVM and allocate qubits
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(200)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    prog = QProg()
    
    if kind == 'full':
        cin = q[0]
        cout = q[2*n + 1]
        a = [q[2*i + 1] for i in range(n)]
        b = [q[2*i + 2] for i in range(n)]
    elif kind == 'half':
        cin = q[2*n + 1]  # helper qubit
        cout = q[2*n]
        a = [q[2*i] for i in range(n)]
        b = [q[2*i + 1] for i in range(n)]
    elif kind == 'fixed':
        cin = q[2*n]      # helper qubit
        cout = q[2*n + 1]  # helper qubit
        a = [q[2*i] for i in range(n)]
        b = [q[2*i + 1] for i in range(n)]
    else:
        raise ValueError("Invalid kind")

    # MAJ gates
    for i in range(n):
        carry = cin if i == 0 else a[i-1]
        x = b[i]
        y = a[i]
        prog << CNOT(y, x)
        prog << CNOT(y, carry)
        prog << X(y).control([x, carry])

    # Copy carry-out
    last_carry = a[n-1]
    prog << CNOT(last_carry, cout)

    # UMA gates
    for i in range(n-1, -1, -1):
        carry = cin if i == 0 else a[i-1]
        x = b[i]
        y = a[i]
        prog << X(y).control([x, carry])
        prog << CNOT(y, carry)
        prog << CNOT(carry, x)

    return prog

machine.finalize()
