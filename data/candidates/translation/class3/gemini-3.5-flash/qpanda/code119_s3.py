# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    # In pyQPanda, we can construct a QCircuit using the CDKM ripple carry adder algorithm.
    # The CDKM adder uses MAJ and UMA gates.
    # Let's define MAJ and UMA as helper functions that append gates to a QCircuit.
    
    def MAJ(c, a, b, circ):
        circ << CNOT(c, b)
        circ << CNOT(c, a)
        circ << Toffoli(a, b, c)

    def UMA(c, a, b, circ):
        circ << Toffoli(a, b, c)
        circ << CNOT(c, a)
        circ << CNOT(a, b)

    # Initialize the machine and qubits
    machine = CPUQVM()
    machine.init_qvm()
    
    # Qiskit CDKMRippleCarryAdder qubits:
    # 'half': 2*n + 1 qubits (a: n, b: n, cout: 1)
    # 'full': 2*n + 2 qubits (cin: 1, a: n, b: n, cout: 1)
    # 'fixed': 2*n + 1 qubits (cin: 1, a: n, b: n)
    
    if kind == 'half':
        num_qubits = 2 * num_state_qubits + 1
    elif kind == 'full':
        num_qubits = 2 * num_state_qubits + 2
    elif kind == 'fixed':
        num_qubits = 2 * num_state_qubits + 1
    else:
        raise ValueError("Invalid kind")
        
    qubits = machine.qAlloc_many(num_qubits)
    circ = QCircuit()
    
    # Map the qubits according to the kind
    if kind == 'full':
        cin = qubits[0]
        a = qubits[1 : num_state_qubits + 1]
        b = qubits[num_state_qubits + 1 : 2 * num_state_qubits + 1]
        cout = qubits[2 * num_state_qubits + 1]
        
        # Carry propagation (MAJ)
        MAJ(cin, b[0], a[0], circ)
        for i in range(1, num_state_qubits):
            MAJ(a[i-1], b[i], a[i], circ)
            
        # Copy carry-out
        circ << CNOT(a[num_state_qubits - 1], cout)
        
        # Reverse carry propagation (UMA)
        for i in reversed(range(1, num_state_qubits)):
            UMA(a[i-1], b[i], a[i], circ)
        UMA(cin, b[0], a[0], circ)
        
    elif kind == 'fixed':
        cin = qubits[0]
        a = qubits[1 : num_state_qubits + 1]
        b = qubits[num_state_qubits + 1 : 2 * num_state_qubits + 1]
        
        # Carry propagation (MAJ)
        MAJ(cin, b[0], a[0], circ)
        for i in range(1, num_state_qubits):
            MAJ(a[i-1], b[i], a[i], circ)
            
        # Reverse carry propagation (UMA)
        for i in reversed(range(1, num_state_qubits)):
            UMA(a[i-1], b[i], a[i], circ)
        UMA(cin, b[0], a[0], circ)
        
    elif kind == 'half':
        a = qubits[0 : num_state_qubits]
        b = qubits[num_state_qubits : 2 * num_state_qubits]
        cout = qubits[2 * num_state_qubits]
        
        # For 'half' adder, Qiskit implements it by using an internal helper qubit
        # which is initialized to 0. But since the CDKMRippleCarryAdder in Qiskit
        # only has 2n+1 qubits, the "cin" is actually mapped to the "cout" qubit
        # which is initially 0.
        # So we use `cout` as the carry-in for the first MAJ.
        cin = cout
        
        # Carry propagation (MAJ)
        MAJ(cin, b[0], a[0], circ)
        for i in range(1, num_state_qubits):
            MAJ(a[i-1], b[i], a[i], circ)
            
        # Copy carry-out
        # In Qiskit's CDKMRippleCarryAdder for 'half', the carry-out is copied
        # to the `cout` qubit. But since `cout` was used as `cin`, we must first
        # restore the `cin` qubit to 0 before copying?
        # Actually, Qiskit does:
        # circ.cx(a[-1], cout)
        # then UMA for i from n-1 down to 1.
        # and then a special block to restore the first stage without using `cout` as control.
