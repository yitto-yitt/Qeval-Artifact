# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, CNOT, Toffoli

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    # Initialize the quantum virtual machine to allocate qubits
    qvm = CPUQVM()
    qvm.init_qvm()
    
    # Determine the number of qubits based on the kind of adder
    if kind == 'full':
        num_qubits = 2 * num_state_qubits + 2
    elif kind == 'half':
        num_qubits = 2 * num_state_qubits + 1
    elif kind == 'fixed':
        num_qubits = 2 * num_state_qubits + 1
    else:
        raise ValueError(f"Unknown kind of adder: {kind}")
        
    qubits = qvm.qAllocMany(num_qubits)
    
    # Assign qubits based on the kind
    if kind == 'full':
        cin = qubits[0]
        a = qubits[1 : num_state_qubits + 1]
        b = qubits[num_state_qubits + 1 : 2 * num_state_qubits + 1]
        cout = qubits[2 * num_state_qubits + 1]
    elif kind == 'half':
        a = qubits[0 : num_state_qubits]
        b = qubits[num_state_qubits : 2 * num_state_qubits]
        cout = qubits[2 * num_state_qubits]
    elif kind == 'fixed':
        cin = qubits[0]
        a = qubits[1 : num_state_qubits + 1]
        b = qubits[num_state_qubits + 1 : 2 * num_state_qubits + 1]
        
    circ = QCircuit()
    
    # Helper functions for MAJ and UMA gates
    def maj(c, a, b):
        circ << CNOT(c, b)
        circ << CNOT(c, a)
        circ << Toffoli(a, b, c)

    def uma(c, a, b):
        circ << Toffoli(a, b, c)
        circ << CNOT(c, a)
        circ << CNOT(a, b)

    # Build the circuit based on the kind of adder
    if kind == 'full':
        # MAJ cascade
        maj(cin, a[0], b[0])
        for i in range(1, num_state_qubits):
            maj(a[i-1], a[i], b[i])
            
        # Copy the final carry to cout
        circ << CNOT(a[num_state_qubits - 1], cout)
        
        # UMA cascade in reverse
        for i in range(num_state_qubits - 1, 0, -1):
            uma(a[i-1], a[i], b[i])
        uma(cin, a[0], b[0])
        
    elif kind == 'half':
        if num_state_qubits > 1:
            # First stage is a half adder
            circ << CNOT(a[0], b[0])
            circ << CNOT(a[0], a[1])
            circ << Toffoli(b[0], a[1], a[0])
            
            # MAJ cascade
            for i in range(2, num_state_qubits):
                maj(a[i-1], a[i], b[i])
                
            # Copy the final carry to cout
            circ << CNOT(a[num_state_qubits - 1], cout)
            
            # UMA cascade in reverse
            for i in range(num_state_qubits - 1, 1, -1):
                uma(a[i-1], a[i], b[i])
                
            # Restore first stage
            circ << Toffoli(b[0], a[1], a[0])
            circ << CNOT(a[0], a[1])
            circ << CNOT(a[0], b[0])
        else:
            # Simple 1-bit half adder
            circ << Toffoli(a[0], b[0], cout)
            circ << CNOT(a[0], b[0])
            
    elif kind == 'fixed':
        # MAJ cascade
        maj(cin, a[0], b[0])
        for i in range(1, num_state_qubits):
            maj(a[i-1], a[i], b[i])
            
        # UMA cascade in reverse
        for i in range(num_state_qubits - 1, 0, -1):
            uma(a[i-1], a[i], b[i])
        uma(cin, a[0], b[0])

    return circ
