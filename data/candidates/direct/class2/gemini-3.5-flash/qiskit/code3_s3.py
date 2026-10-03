# EVAL_META: task_id=3, framework=qiskit, class=2

from qiskit import QuantumCircuit

def create_ghz(drawing=False):
    # Create a Quantum Circuit with 3 qubits and 3 classical bits
    qc = QuantumCircuit(3, 3)
    
    # Generate the GHZ state
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    
    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])
    
    if drawing:
        fig = qc.draw(output='mpl')
        return qc, fig
    else:
        return qc
