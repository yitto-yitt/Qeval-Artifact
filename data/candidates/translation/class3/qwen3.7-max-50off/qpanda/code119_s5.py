# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind == 'half':
        num_qubits = 2 * n + 1
    else:
        kind = 'full'
        num_qubits = 2 * n + 2
        
    qc = QuantumCircuit(num_qubits)
    
    def maj(x, y, z):
        qc.cx(z, y)
        qc.cx(z, x)
        qc.ccx(x, y, z)

    def uma(x, y, z):
        qc.ccx(x, y, z)
        qc.cx(z, x)
        qc.cx(x, y)
        
    def maj_half(y, z):
        qc.cx(z, y)
        
    def uma_half(y, z):
        pass

    cout = 2 * n if kind == 'half' else 2 * n + 1
    cin = 2 * n if kind == 'full' else None

    if n == 1:
        if kind == 'full':
            maj(cin, n, 0)
            qc.cx(0, cout)
            uma(cin, n, 0)
        else:
            maj_half(n, 0)
            qc.cx(0, cout)
            uma_half(n, 0)
    else:
        if kind == 'full':
            maj(cin, n, 0)
            for i in range(n - 1):
                maj(i, n + i + 1, i + 1)
            qc.cx(n - 1, cout)
            for i in reversed(range(n - 1)):
                uma(i, n + i + 1, i + 1)
            uma(cin, n, 0)
        else:
            maj_half(n, 0)
            for i in range(n - 1):
                maj(i, n + i + 1, i + 1)
            qc.cx(n - 1, cout)
            for i in reversed(range(n - 1)):
                uma(i, n + i + 1, i + 1)
            uma_half(n, 0)

    return qc
