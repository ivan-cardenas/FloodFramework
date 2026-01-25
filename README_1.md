# Circular Dendrogram Explorer

A beautiful, interactive Streamlit application for visualizing hierarchical data using circular dendrograms with dynamic filtering capabilities.

## Features

- 📊 **Interactive Circular Dendrogram**: Beautiful radial visualization of hierarchical relationships
- 🎯 **Two-Level Filtering**: Filter by both category and subcategory
- 🎨 **Modern Design**: Clean, gradient interface with custom styling
- 📥 **CSV Upload**: Easy data import via drag-and-drop
- 💾 **Export Filtered Data**: Download your filtered results
- 📈 **Real-time Updates**: Dendrogram regenerates automatically when filters change
- 🎨 **Color-Coded Categories**: Each category gets a unique color for easy identification

## Installation

1. **Clone or download the files**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Running the App

```bash
streamlit run circular_dendrogram_app.py
```

The app will open in your default web browser at `http://localhost:8501`

### Using the App

1. **Upload CSV File**
   - Click "Browse files" in the sidebar
   - Select your CSV file (must have at least 2 columns)

2. **Configure Columns**
   - Select your **Category Column** (main grouping level - outer ring)
   - Select your **Subcategory Column** (sub-grouping level - inner ring)

3. **Filter Data**
   - Use the Category filter to include/exclude entire categories
   - Use the Subcategory filter to include/exclude specific subcategories
   - The dendrogram updates automatically

4. **Explore**
   - Hover over nodes to see details
   - View statistics in the metrics panel
   - Expand "View Filtered Data" to see the underlying data
   - Download filtered data as CSV

## CSV Format

Your CSV should have at least two columns representing hierarchical levels:

```csv
Category,Subcategory,Value
Technology,Software,120
Technology,Hardware,85
Finance,Banking,200
Finance,Insurance,150
Healthcare,Hospitals,250
```

**Column Requirements:**
- Minimum 2 columns (category and subcategory)
- Additional columns are optional (can be used for reference)
- No specific naming requirements - you select columns in the app

## Sample Data

A sample CSV file (`sample_data.csv`) is included with example hierarchical data across 6 categories:
- Technology
- Finance
- Healthcare
- Education
- Marketing
- Operations

## How the Visualization Works

### Circular Dendrogram Structure

- **Center**: Empty space for clarity
- **Inner Ring**: Category nodes (larger, labeled)
- **Outer Ring**: Subcategory nodes (smaller, size varies by count)
- **Lines**: Connect categories to their subcategories

### Color Scheme

Each category is assigned a unique color from a carefully selected palette:
- Colors are consistent throughout the session
- Subcategories inherit their parent category's color
- Node sizes reflect the number of records in each subcategory

### Interactive Features

- **Hover**: See category, subcategory, and count information
- **Zoom**: Click and drag to pan, scroll to zoom
- **Filter**: Multiselect dropdowns for both levels
- **Reset**: Simply reselect categories/subcategories

## Customization

### Modify Colors

Edit the `colors` list in the `create_circular_dendrogram()` function:

```python
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', ...]  # Add your hex colors
```

### Adjust Node Sizes

Modify the size calculation in the dendrogram function:

```python
node_sizes.append(10 + count * 2)  # Change multiplier for different sizing
```

### Change Layout

Adjust the gradient background in the CSS section:

```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## Technical Details

### Libraries Used

- **Streamlit**: Web app framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations
- **SciPy**: Hierarchical clustering algorithms

### Performance

- Handles datasets with hundreds of categories/subcategories
- Real-time filtering with instant updates
- Responsive design works on different screen sizes

## Troubleshooting

**Issue**: Dendrogram looks crowded
- **Solution**: Use filters to reduce the number of visible categories

**Issue**: Labels overlapping
- **Solution**: The app automatically adjusts text size, but you can zoom in for better readability

**Issue**: Colors not distinct enough
- **Solution**: Modify the color palette in the code

**Issue**: Upload fails
- **Solution**: Ensure CSV is properly formatted with column headers

## Future Enhancements

Potential features for future versions:
- [ ] Export dendrogram as image (PNG/SVG)
- [ ] Support for more than 2 hierarchical levels
- [ ] Value-weighted node sizing
- [ ] Theme customization options
- [ ] Search functionality for specific nodes
- [ ] Comparison mode for multiple datasets

## License

Free to use and modify for your projects.

## Author

Created with expertise in geospatial analysis, data visualization, and graphic design.

---

**Enjoy exploring your data! 🌳**
