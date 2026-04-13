# IFS Fractal Visualizer 🌀

An interactive web application for exploring custom fractals using Iterated Function Systems (IFS) with matrix transformations. Adjust parameters in real-time and see the fractal update instantly with transformation statistics.

## Features

- **Interactive Fractal Generation**: Adjust transformation parameters (a, b, c, d, e, f) with sliders
- **Real-time Visualization**: See fractals update instantly as you modify parameters
- **Color-Coded Transformations**: Each point is colored by the transformation that created it
- **Dimension Calculation**: Automatic Hausdorff dimension estimation
- **Transformation Statistics**: View distribution of transformation usage across points
- **Customizable Presets**: Choose 1-8 transformations
- **Point Control**: Adjust point count from 500 to 50,000

## Mathematical Background

### Affine Transformations
Each transformation applies:
```
[x']   [a  b] [x]   [e]
[y'] = [c  d] [y] + [f]
```

### Chaos Game Algorithm
1. Start at origin (0, 0)
2. Randomly select a transformation
3. Apply it to current point
4. Repeat N times, tracking which transformation was used

### Hausdorff Dimension
```
D = ln(n) / ln(1/r)
```
where n = number of transformations, r = average contraction ratio

## Default: Sierpinski Triangle

- T1: a=0.5, b=0, c=0, d=0.5, e=0, f=0
- T2: a=0.5, b=0, c=0, d=0.5, e=0.5, f=0
- T3: a=0.5, b=0, c=0, d=0.5, e=0.25, f=0.432
- **Dimension: 1.585**

## Installation & Local Run

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/fractal-visualizer.git
cd fractal-visualizer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy and share the app:

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repo, branch, and `app.py` file
   - Click "Deploy"

3. **Share the link** - Anyone can now use your app in their browser!

### Option 2: GitHub Pages + GitHub Actions

Deploy as a static site with a backend service:

1. Create `.github/workflows/deploy.yml`
2. Configure action to build and serve the app
3. Requires additional setup with a backend server

### Option 3: Self-Hosted

Deploy on your own server using Docker or Heroku:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["streamlit", "run", "app.py"]
```

## Usage Guide

### Creating Custom Fractals

1. **Set transformations**: Choose 1-8 transformations
2. **Adjust parameters**: Use sliders for each coefficient
3. **Control detail**: Increase points for finer detail (slower)
4. **Observe patterns**: Color distribution shows transformation usage

### Parameter Ranges

All parameters are constrained to [0, 1] for **stable, convergent fractals**:
- **a, d**: Diagonal scaling (main contraction)
- **b, c**: Off-diagonal rotation/shearing
- **e, f**: Translation (positioning)

### Tips

- Start low values (0.3-0.5) for a, d for clear fractals
- Use e, f symmetrically for centered fractals
- Increase point count to reduce noise
- Experiment with slight variations to discover new patterns

## Examples

### Sierpinski Carpet (8 transformations)
- All: a=0.333, b=0, c=0, d=0.333
- Positions: 3×3 grid (skip center)
- Dimension: 1.893

### Random Variations
- Try: a=0.4, b=0.1, c=0.1, d=0.4 (with different e, f)
- Explore: Chaotic-looking but self-similar patterns

## Project Structure

```
fractal-visualizer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore         # Git ignore file
└── .github/
    └── workflows/     # GitHub Actions (optional)
```

## Technical Details

### Performance
- Vectorized NumPy operations for speed
- matplotlib for rendering
- Streamlit caching for interactive responsiveness

### Browser Compatibility
- Chrome, Firefox, Safari, Edge (latest)
- Requires JavaScript enabled
- Mobile-friendly responsive design

## Future Enhancements

- [ ] Export fractal as high-res PNG/SVG
- [ ] Pre-built fractal gallery
- [ ] Animation: smooth parameter transitions
- [ ] 3D fractal visualization
- [ ] Probability weights for transformations
- [ ] Save/load custom fractals

## License

MIT License - Feel free to use and modify!

## Author

Created for MATH311: Fractal Geometry course

## Questions or Issues?

- Open an issue on GitHub
- Check the [Streamlit documentation](https://docs.streamlit.io)
- Review [Fractals and Self-Similarity](https://en.wikipedia.org/wiki/Fractal)

---

**Try it now**: [Visit the deployed app](https://share.streamlit.io) (after deployment)
