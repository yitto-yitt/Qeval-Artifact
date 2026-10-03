# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq
from qiskit.circuit.library import CDKMRippleCarryAdder
from qiskit import QuantumCircuit, transpile

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    # Create the Qiskit CDKMRippleCarryAdder
    adder = CDKMRippleCarryAdder(num_state_qubits, kind)
    
    # Build the Qiskit QuantumCircuit
    qc = QuantumCircuit(adder.num_qubits)
    qc.append(adder.to_instruction(), range(adder.num_qubits))
    
    # Transpile to basis gates 'cx' and 'ccx'
    qc_decomposed = transpile(qc, basis_gates=['cx', 'ccx'], optimization_level=0)
    
    # Translate to pyQPanda QCircuit
    pyqpanda_circuit = pq.QCircuit()
    
    for instruction in qc_decomposed.data:
        gate_name = instruction.operation.name
        qubits = instruction.qubits
        q_indices = [qc_decomposed.qubits.index(qubit) for qubit in qubits]
        
        if gate_name == 'cx':
            pyqpanda_circuit << pq.CNOT(global_qubits[q_indices[0]], global_qubits[q_indices[1]])
        elif gate_name == 'ccx':
            ctrl_qubits = pq.QVec()
            ctrl_qubits.append(global_qubits[q_indices[0]])
            ctrl_qubits.append(global_qubits[q_indices[1]])
            pyqpanda_circuit << pq.X(global_qubits[q_indices[2]]).control(ctrl_qubits)
            
    return pyqpanda_circuit

# Manual Cleanup
machine.finalize()
