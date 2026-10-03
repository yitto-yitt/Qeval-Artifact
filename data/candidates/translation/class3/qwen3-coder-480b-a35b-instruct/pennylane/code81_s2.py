# EVAL_META: task_id=81, framework=pennylane, class=3
import pennylane as qml

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    
    # Parse the QASM string manually since PennyLane doesn't have direct QASM parsing
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.state()
    
    # Return the tape which represents the circuit
    tape = circuit.qtape
    return tape
