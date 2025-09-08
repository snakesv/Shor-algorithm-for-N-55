from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from numpy import pi

def create_quantum_registers(num_qubits: int = 10, num_classical: int = 4) -> tuple:
    """
    Create quantum and classical registers for the circuit.
    
    Args:
        num_qubits (int): Number of quantum bits
        num_classical (int): Number of classical bits
    
    Returns:
        tuple: Quantum register, Classical register, and Quantum circuit
    """
    q = QuantumRegister(num_qubits, 'q')
    c = ClassicalRegister(num_classical, 'c')
    circuit = QuantumCircuit(q, c)
    return q, c, circuit

def initialize_circuit(circuit: QuantumCircuit, q: QuantumRegister) -> None:
    """
    Initialize the quantum circuit with initial states and superposition.
    
    Args:
        circuit (QuantumCircuit): The quantum circuit
        q (QuantumRegister): The quantum register
    """
    # Set |1> state
    circuit.x(q[0])
    
    # Create superposition
    for i in range(6, 10):
        circuit.h(q[i])
    circuit.barrier()

def apply_controlled_operations(circuit: QuantumCircuit, q: QuantumRegister) -> None:
    """
    Apply controlled unitary operations to the circuit.
    
    Args:
        circuit (QuantumCircuit): The quantum circuit
        q (QuantumRegister): The quantum register
    """
    # U^2^0
    circuit.cx(q[6],q[3])
    circuit.cx(q[6],q[2])
    circuit.cx(q[6],q[0])
    circuit.barrier()

    #U^2^1
    circuit.cx(q[7],q[0])
    circuit.cx(q[7],q[1])
    circuit.ccx (q[7], q[2], q[3])
    circuit.ccx (q[7], q[2], q[4])
    circuit.x(q[4])
    circuit.ccx (q[7], q[4], q[5])
    circuit.x(q[4])
    circuit.barrier()

def apply_inverse_qft(circuit: QuantumCircuit, q: QuantumRegister) -> None:
    """
    Apply inverse Quantum Fourier Transform on qubits 6-9.
    Matches exactly with the original circuit implementation.
    
    Args:
        circuit (QuantumCircuit): The quantum circuit
        q (QuantumRegister): The quantum register
    """
    # Step 1: Initial SWAP operations
    circuit.swap(q[7], q[8])
    circuit.swap(q[6], q[9])

    # Step 2: Qubit 6
    circuit.h(q[6])
    circuit.cp(-pi/2, q[6], q[7])

    # Step 3: Qubit 7
    circuit.h(q[7])
    circuit.cp(-pi/4, q[6], q[8])
    circuit.cp(-pi/2, q[7], q[8])

    # Step 4: Qubit 8
    circuit.h(q[8])
    circuit.cp(-pi/8, q[6], q[9])
    circuit.cp(-pi/4, q[7], q[9])
    circuit.cp(-pi/2, q[8], q[9])

    # Step 5: Final Hadamard on qubit 9
    circuit.h(q[9])

    # Add barrier for clarity
    circuit.barrier()
def measure_circuit(circuit: QuantumCircuit, q: QuantumRegister, c: ClassicalRegister) -> None:
    """
    Add measurement operations to the circuit.
    
    Args:
        circuit (QuantumCircuit): The quantum circuit
        q (QuantumRegister): The quantum register
        c (ClassicalRegister): The classical register
    """
    for i in range(4):
        circuit.measure(q[i+6], c[i])

def run_simulation(circuit: QuantumCircuit) -> dict:
    """
    Run the quantum circuit simulation and process results.
    
    Args:
        circuit (QuantumCircuit): The quantum circuit to simulate
    
    Returns:
        dict: Processed measurement results in decimal format
    """
    # Initialize simulator and run
    aersim = AerSimulator()
    result_ideal = aersim.run(circuit).result()
    counts_ideal = result_ideal.get_counts(0)
    
    # Sort results by count
    sorted_counts = dict(sorted(counts_ideal.items(), key=lambda item: -item[1]))
    
    # Convert binary results to decimal
    decimal_counts = {}
    for binary_state, count in sorted_counts.items():
        binary_clean = binary_state.replace(" ", "")
        decimal_value = int(binary_clean, 2)
        decimal_counts[str(decimal_value)] = count
    
    return decimal_counts
def visualize_results(circuit: QuantumCircuit, decimal_counts: dict) -> None:
    """
    Visualize the circuit and measurement results.
    
    Args:
        circuit (QuantumCircuit): The quantum circuit
        decimal_counts (dict): The measurement results in decimal format
    """
    # Draw circuit
    circuit.draw(output="mpl", fold=1)
    plt.show()
    
    # Plot histogram of results
    plot_histogram(decimal_counts, sort='value', title='Result').show()
    plt.show()
def main():
    """
    Main function to execute the quantum factoring algorithm.
    """
    # Create circuit
    q, c, circuit = create_quantum_registers()
    
    # Build circuit
    initialize_circuit(circuit, q)
    apply_controlled_operations(circuit, q)
    apply_inverse_qft(circuit, q)
    measure_circuit(circuit, q, c)
    
    # Run and visualize
    results = run_simulation(circuit)
    visualize_results(circuit, results)

if __name__ == "__main__":
    main()