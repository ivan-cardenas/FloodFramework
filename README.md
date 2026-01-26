# Flood Risk Framework - Dendrogram Explorer

A beautiful, interactive Streamlit application for visualizing hierarchical data using circular dendrograms with dynamic filtering capabilities.

## Features

- 📊 **Interactive Flood Risk Framework Dendrogram**: Beautiful radial visualization of hierarchical relationships
- 🎯 **Two-Level Filtering**: Filter by both category and subcategory
- 🎨 **Modern Design**: Clean, gradient interface with custom styling
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


1. **Configure Columns**
   - Select your **Category Column** (main grouping level - outer ring)
   - Select your **Subcategory Column** (sub-grouping level - inner ring)

2. **Filter Data**
   - Use the Category filter to include/exclude entire categories
   - Use the Subcategory filter to include/exclude specific subcategories
   - The dendrogram updates automatically

3. **Explore**
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


## Customization

### Modify Colors

Edit the `colors` list in the `create_circular_dendrogram()` function:

```python
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', ...]  # Add your hex colors
```

### Adjust Node Sizes

Modify the size calculation in the dendrogram function:

```python
symbol_size = 15  # Change value for different sizing
```

### Change Layout

Adjust the gradient background in the CSS section:

```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## Technical Details

### Libraries Used

- **Streamlit**: Web app framework
- **Pyecharts**: Interactive visualizations
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


## Future Enhancements

Potential features for future versions:
- [ ] Export dendrogram as image (PNG/SVG)
- [ ] Support for more than 2 hierarchical levels
- [ ] Value-weighted node sizing
- [ ] Theme customization options
- [ ] Search functionality for specific nodes
- [ ] Comparison mode for multiple datasets

## License

This project is released under the [CC-BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.

## Authors

Created with expertise in geospatial analysis, data visualization, and graphic design.

---

**Enjoy exploring your data! 🌳**
