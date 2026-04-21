import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Set page config
st.set_page_config(
    page_title="IFS Fractal Visualizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5em;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    .section-header {
        font-size: 1.3em;
        font-weight: bold;
        color: #666;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 2px solid #ddd;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

class MatrixIFS:
    """
    Iterated Function System using affine matrix transformations.
    
    Each transformation is defined by: new_point = M · point + t
    Where M is a 2x2 matrix [[a, b], [c, d]] and t is translation [e, f]
    """
    def __init__(self, matrices, translations, probabilities=None):
        """
        Parameters:
        - matrices: list of 2x2 transformation matrices [[a, b], [c, d]]
        - translations: list of translation vectors [e, f]
        - probabilities: weights for each transformation (default: uniform)
        """
        self.matrices = np.array(matrices)
        self.translations = np.array(translations)
        self.n_transforms = len(matrices)
        
        if probabilities is None:
            self.probabilities = np.ones(self.n_transforms) / self.n_transforms
        else:
            self.probabilities = np.array(probabilities)
            self.probabilities = self.probabilities / np.sum(self.probabilities)
    
    def compute(self, num_points):
        """Generate fractal using chaos game with matrix transformations"""
        np.random.seed(42)
        
        # Start at origin
        point = np.array([0.0, 0.0])
        points = np.zeros((num_points, 2))
        
        # Generate all random transformation indices upfront (vectorized)
        indices = np.random.choice(self.n_transforms, size=num_points, 
                                   p=self.probabilities)
        
        # Apply transformations sequentially
        for i in range(num_points):
            idx = indices[i]
            # Matrix-vector multiplication: M @ point
            point = self.matrices[idx] @ point + self.translations[idx]
            points[i] = point
        
        #Store transformation indices for tracking
        self.last_indices = indices
        return points
    
    def estimate_dimension(self):
        """
        Estimate fractal dimension using box dimension approach.
        For a self-affine fractal: D ≈ log(n) / log(1/r)
        where n is number of transformations and r is average contraction ratio.
        """
        # Compute contraction ratios from eigenvalues of transformation matrices
        contraction_ratios = []
        for matrix in self.matrices:
            eigenvalues = np.linalg.eigvals(matrix)
            avg_contraction = np.mean(np.abs(eigenvalues))
            contraction_ratios.append(avg_contraction)
        
        r_avg = np.mean(contraction_ratios)
        
        if r_avg < 1e-10:  # Avoid division by zero
            return None
        
        #Dimension formula: ln(n) / ln(1/r)
        dimension = np.log(self.n_transforms) / np.log(1 / r_avg)
        return dimension


# Page Title
st.markdown('<div class="main-title"> IFS Fractal Visualizer</div>', unsafe_allow_html=True)
st.write("Explore custom fractals by adjusting transformation parameters. Each point is colored by the transformation that created it.")

# Sidebar for controls
st.sidebar.markdown('<div class="section-header">Fractal Parameters</div>', unsafe_allow_html=True)

# Visualization mode selector
visualization_mode = st.sidebar.radio(
    "Visualization Mode",
    options=['Scatter (Triangle)', 'Density (Gasket)'],
    index=0,
    help="Scatter: Point-based chaos game | Density: Filled heat map"
)

# Number of transformations
n_transforms = st.sidebar.slider(
    "Number of Transformations",
    min_value=1,
    max_value=50,
    value=3,
    help="Number of transformation functions (1-50)"
)

# Number of points
num_points = st.sidebar.slider(
    "Points",
    min_value=500,
    max_value=50000,
    value=5000,
    step=500,
    help="Number of points to compute for the fractal"
)

# Sierpinski defaults
sierpinski_defaults = [
    {'a': 0.5, 'b': 0.0, 'c': 0.0, 'd': 0.5, 'e': 0.0, 'f': 0.0},
    {'a': 0.5, 'b': 0.0, 'c': 0.0, 'd': 0.5, 'e': 0.5, 'f': 0.0},
    {'a': 0.5, 'b': 0.0, 'c': 0.0, 'd': 0.5, 'e': 0.25, 'f': 0.432},
]

# Build transformation parameters
st.sidebar.markdown('<div class="section-header">Transformations (T#: a,b,c,d,e,f)</div>', unsafe_allow_html=True)

transform_params = {}
for i in range(n_transforms):
    st.sidebar.write(f"**T{i+1}**")
    cols = st.sidebar.columns(6)
    
    if i < len(sierpinski_defaults):
        defaults = sierpinski_defaults[i]
    else:
        defaults = {'a': 0.5, 'b': 0.0, 'c': 0.0, 'd': 0.5, 'e': 0.0, 'f': 0.0}
    
    transform_params[i] = {
        'a': cols[0].number_input(f'a{i+1}', value=defaults['a'], min_value=-1.0, max_value=1.0, step=0.01, label_visibility="collapsed"),
        'b': cols[1].number_input(f'b{i+1}', value=defaults['b'], min_value=-1.0, max_value=1.0, step=0.01, label_visibility="collapsed"),
        'c': cols[2].number_input(f'c{i+1}', value=defaults['c'], min_value=-1.0, max_value=1.0, step=0.01, label_visibility="collapsed"),
        'd': cols[3].number_input(f'd{i+1}', value=defaults['d'], min_value=-1.0, max_value=1.0, step=0.01, label_visibility="collapsed"),
        'e': cols[4].number_input(f'e{i+1}', value=defaults['e'], min_value=-1.0, max_value=1.0, step=0.01, label_visibility="collapsed"),
        'f': cols[5].number_input(f'f{i+1}', value=defaults['f'], min_value=-1.0, max_value=1.0, step=0.01, label_visibility="collapsed"),
    }

# Build matrices and translations
matrices = []
translations = []
for i in range(n_transforms):
    matrix = np.array([
        [transform_params[i]['a'], transform_params[i]['b']],
        [transform_params[i]['c'], transform_params[i]['d']]
    ])
    translation = np.array([
        transform_params[i]['e'],
        transform_params[i]['f']
    ])
    matrices.append(matrix)
    translations.append(translation)

# Compute fractal
try:
    ifs = MatrixIFS(matrices, translations)
    points = ifs.compute(num_points)
    dimension = ifs.estimate_dimension()
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
    
    # Calculate bounds from actual points
    x_vals = points[:, 0]
    y_vals = points[:, 1]
    
    if not (np.all(np.isnan(x_vals)) or np.all(np.isnan(y_vals))):
        x_min, x_max = np.nanmin(x_vals), np.nanmax(x_vals)
        y_min, y_max = np.nanmin(y_vals), np.nanmax(y_vals)
        
        # Add padding
        x_range = x_max - x_min if x_max != x_min else 1.0
        y_range = y_max - y_min if y_max != y_min else 1.0
        padding = 0.1
        
        x_min -= x_range * padding
        x_max += x_range * padding
        y_min -= y_range * padding
        y_max += y_range * padding
        
        # Color map for transformations (50 distinct colors)
        colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray',
                  '#FF6347', '#4169E1', '#32CD32', '#FFD700', '#FF1493', '#00CED1',
                  '#FF8C00', '#20B2AA', '#DC143C', '#6495ED', '#228B22', '#FFB6C1',
                  '#8B4513', '#00BFFF', '#8B008B', '#FF4500', '#2F4F4F', '#FF69B4',
                  '#696969', '#ADFF2F', '#1E90FF', '#FF00FF', '#3CB371', '#8B0000',
                  '#FF7F50', '#1C1C1C', '#556B2F', '#9932CC', '#FF69B4', '#F08080',
                  '#00008B', '#008000', '#4B0082', '#F0E68C', '#00FA9A', '#90EE90',
                  '#00FFFF', '#191970', '#FFA500', '#FFB6C1', '#FFC0CB', '#FF00FF']
        
        if visualization_mode == 'Scatter (Triangle)':
            # Plot points colored by transformation index (Scatter mode)
            point_count = 0
            for t_idx in range(n_transforms):
                mask = ifs.last_indices == t_idx
                if np.any(mask):
                    valid_mask = ~np.isnan(x_vals[mask]) & ~np.isnan(y_vals[mask])
                    if np.any(valid_mask):
                        ax.scatter(x_vals[mask][valid_mask], y_vals[mask][valid_mask], 
                                  s=2, c=colors[t_idx % len(colors)], alpha=0.7, 
                                  label=f'T{t_idx+1}')
                        point_count += np.sum(valid_mask)
            if point_count > 0:
                ax.legend(loc='upper right', fontsize=8)
        else:
            # Create 2D histogram for density visualization (Gasket mode)
            valid_mask = ~np.isnan(x_vals) & ~np.isnan(y_vals)
            if np.any(valid_mask):
                x_valid = x_vals[valid_mask]
                y_valid = y_vals[valid_mask]
                
                # Create bins for histogram
                bins = int(np.sqrt(num_points / 10))
                bins = max(20, min(bins, 100))  # Constrain bin count
                
                # Plot 2D histogram with heatmap
                h = ax.hist2d(x_valid, y_valid, bins=bins, cmap='hot')
                plt.colorbar(h[3], ax=ax, label='Point Density')
        
        # Title
        mode_label = 'Scatter' if visualization_mode == 'Scatter (Triangle)' else 'Density'
        title = f'{mode_label} - Custom Fractal (n={n_transforms}, {num_points} points)'
        if dimension is not None:
            title += f' | D={dimension:.3f}'
        
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_aspect('equal')
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.grid(True, alpha=0.2)
        
        plt.tight_layout()
        
        # Display plot
        col1, col2 = st.columns([3, 1])
        with col1:
            st.pyplot(fig)
        
        # Display stats in sidebar
        with col2:
            st.markdown('<div class="section-header">Statistics</div>', unsafe_allow_html=True)
            
            # Transformation distribution
            unique, counts = np.unique(ifs.last_indices, return_counts=True)
            stats = {int(t): int(count) for t, count in zip(unique, counts)}
            
            st.write("**Transformation Distribution:**")
            for t_idx in sorted(stats.keys()):
                pct = (stats[t_idx] / sum(stats.values())) * 100
                st.write(f"T{t_idx+1}: {stats[t_idx]:,} ({pct:.1f}%)")
            
            if dimension is not None:
                st.write(f"\n**Dimension: {dimension:.4f}**")
    else:
        st.error("Invalid fractal: All points collapsed. Try adjusting transformation parameters.")
        
except Exception as e:
    st.error(f"Error computing fractal: {e}")

# Information section
st.markdown("---")
st.markdown("""
### Info:

Each **transformation** is defined by an affine matrix operation:
$$\\begin{pmatrix} x' \\\\ y' \\end{pmatrix} = \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} \\begin{pmatrix} x \\\\ y \\end{pmatrix} + \\begin{pmatrix} e \\\\ f \\end{pmatrix}$$

The **Hausdorff dimension** is estimated as:
$$D = \\frac{\\ln(n)}{\\ln(1/r)}$$
where *n* = number of transformations and *r* = average contraction ratio.

""")
