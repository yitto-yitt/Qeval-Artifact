# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    def cx_chain_full():
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 4])
    
    u_full = qml.matrix(cx_chain_full, wire_order=[0, 1, 2, 3, 4])()
    
    with qml.tape.QuantumTape() as tape_full:
        qml.Hadamard(wires=0)
        qml.QubitUnitary(u_full, wires=[0, 1, 2, 3, 4])
        
    def cx_chain_1():
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
    u_1 = qml.matrix(cx_chain_1, wire_order=[0, 1, 2])()
    
    def cx_chain_2():
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 4])
    u_2 = qml.matrix(cx_chain_2, wire_order=[2, 3, 4])()
    
    with qml.tape.QuantumTape() as tape_limited:
        qml.Hadamard(wires=0)
        qml.QubitUnitary(u_1, wires=[0, 1, 2])
        qml.QubitUnitary(u_2, wires=[2, 3, 4])
        
    return tape_full, tape_limited
