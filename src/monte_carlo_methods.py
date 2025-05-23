import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
n_samples = 10000  # Number of samples
x_range = (-5, 5)  # Range for visualization
x_vals = np.linspace(*x_range, 1000)  # For plotting

# ========== Distribution Definitions ==========
def target_distribution(x):
    """Bimodal mixture of two normal distributions."""
    return 0.5 * norm.pdf(x, loc=-2, scale=0.5) + 0.5 * norm.pdf(x, loc=2, scale=0.5)

def proposal_distribution(x):
    """Proposal distribution for importance sampling (single normal)."""
    return norm.pdf(x, loc=0, scale=2)

# ========== Sampling Methods ==========
def standard_monte_carlo(n_samples):
    """Standard Monte Carlo sampling from uniform distribution."""
    samples = np.random.uniform(*x_range, n_samples)
    weights = np.ones(n_samples) / n_samples
    return samples, weights

def importance_sampling(n_samples):
    """Importance sampling using the proposal distribution."""
    # Sample from proposal (normal distribution)
    samples = np.random.normal(loc=0, scale=2, size=n_samples)
    # Calculate weights
    weights = target_distribution(samples) / proposal_distribution(samples)
    weights /= np.sum(weights)  # Normalize weights
    return samples, weights

def metropolis_hastings(n_samples, initial_x=0, proposal_std=1):
    """Metropolis-Hastings MCMC algorithm."""
    samples = [initial_x]
    current_x = initial_x
    
    for _ in range(n_samples - 1):
        # Propose new sample
        proposed_x = np.random.normal(current_x, proposal_std)
        
        # Calculate acceptance probability
        acceptance_ratio = target_distribution(proposed_x) / target_distribution(current_x)
        
        # Accept or reject
        if np.random.rand() < min(1, acceptance_ratio):
            current_x = proposed_x
        samples.append(current_x)
    
    samples = np.array(samples)
    weights = np.ones(n_samples) / n_samples  # Equal weights for MCMC
    return samples, weights

# ========== Generate Samples ==========
# Generate samples from each method
mc_samples, mc_weights = standard_monte_carlo(n_samples)
is_samples, is_weights = importance_sampling(n_samples)
mh_samples, mh_weights = metropolis_hastings(n_samples)

# Calculate means (theoretical expectation is 0)
mc_mean = np.sum(mc_samples * mc_weights)
is_mean = np.sum(is_samples * is_weights)
mh_mean = np.sum(mh_samples * mh_weights)

# ========== Visualization ==========
plt.figure(figsize=(12, 8))

# Plot target distribution
plt.plot(x_vals, target_distribution(x_vals), 'k-', 
         label='Target Distribution', linewidth=2)

# Plot sampling distributions
plt.hist(mc_samples, bins=50, density=True, alpha=0.3, 
         label='Standard MC', color='blue')
plt.hist(is_samples, bins=50, density=True, alpha=0.3, 
         label='Importance Sampling', color='green', weights=is_weights)
plt.hist(mh_samples, bins=50, density=True, alpha=0.3, 
         label='Metropolis-Hastings', color='red')

# Add mean lines
plt.axvline(mc_mean, color='blue', linestyle='--', 
            label=f'Standard MC Mean: {mc_mean:.3f}')
plt.axvline(is_mean, color='green', linestyle='--', 
            label=f'Importance Sampling Mean: {is_mean:.3f}')
plt.axvline(mh_mean, color='red', linestyle='--', 
            label=f'MH Mean: {mh_mean:.3f}')

# Formatting
plt.title('Comparison of Sampling Methods for Bimodal Distribution')
plt.xlabel('x')
plt.ylabel('Density')
plt.legend()
plt.grid(True)

# Save and show
plt.savefig('sampling_comparison.png')
plt.show()