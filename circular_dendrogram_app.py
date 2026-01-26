import streamlit as st
import pandas as pd
from pathlib import Path
# import plotly.graph_objects as go
from pyecharts import options as opts
from pyecharts.charts import Tree
import streamlit.components.v1 as components
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
import io


THIS_DIR = Path(__file__).resolve().parent
DATA_DIR = THIS_DIR / "data"

# Page configuration
st.set_page_config(
    page_title="Flood Framework",
    page_icon="",
    layout="wide"
)

# Custom CSS for better design
st.markdown("""
    <style>219ebc
    .main {
        padding: 2rem;
    }
    .stApp {
        background: linear-gradient(135deg, #023047 0%, #219ebc 100%);
    }
    .css-1d391kg {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# def create_circular_dendrogram(df, category_col, subcategory_col, value_col=None):
#     """
#     Create a circular dendrogram from hierarchical data
    
#     Parameters:
#     - df: DataFrame with hierarchical data
#     - category_col: Column name for main categories
#     - subcategory_col: Column name for subcategories
#     - value_col: Optional column for values/weights
#     """
    
#     # Create hierarchical structure
#     categories = df[category_col].unique()
    
#     # Build coordinates for circular layout
#     nodes = []
#     node_colors = []
#     node_sizes = []
    
#     # Color palette for categories
#     colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
#               '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']
    
#     category_colors = {cat: colors[i % len(colors)] for i, cat in enumerate(categories)}
    
#     # Calculate positions
#     total_items = len(df)
#     angle_step = 2 * np.pi / total_items
    
#     edges_x = []
#     edges_y = []
    
#     current_angle = 0
#     category_positions = {}
    
#     for category in categories:
#         cat_df = df[df[category_col] == category]
#         subcats = cat_df[subcategory_col].unique()
        
#         cat_start_angle = current_angle
        
#         for subcat in subcats:
#             subcat_df = cat_df[cat_df[subcategory_col] == subcat]
#             count = len(subcat_df)
            
#             # Position for this subcategory
#             mid_angle = current_angle + (count * angle_step) / 2
            
#             # Outer radius for leaf nodes
#             radius = 1.0
#             x = radius * np.cos(mid_angle)
#             y = radius * np.sin(mid_angle)
            
#             nodes.append({
#                 'x': x, 
#                 'y': y, 
#                 'category': category,
#                 'subcategory': subcat,
#                 'count': count,
#                 'angle': mid_angle
#             })
            
#             node_colors.append(category_colors[category])
#             node_sizes.append(10 + count * 2)  # Size based on count
            
#             current_angle += count * angle_step
        
#         # Store category center
#         cat_end_angle = current_angle
#         cat_mid_angle = (cat_start_angle + cat_end_angle) / 2
#         category_positions[category] = {
#             'angle': cat_mid_angle,
#             'x': 0.5 * np.cos(cat_mid_angle),
#             'y': 0.5 * np.sin(cat_mid_angle)
#         }
    
#     # Create edges connecting subcategories to categories
#     for node in nodes:
#         cat_pos = category_positions[node['category']]
        
#         # Draw edge from category center to subcategory
#         edges_x.extend([cat_pos['x'], node['x'], None])
#         edges_y.extend([cat_pos['y'], node['y'], None])
    
#     # Create the plot
#     fig = go.Figure()
    
#     # Add edges
#     fig.add_trace(go.Scatter(
#         x=edges_x,
#         y=edges_y,
#         mode='lines',
#         line=dict(color='#023047', width=1),
#         hoverinfo='none',
#         showlegend=False
#     ))
    
#     # Add category nodes (inner circle)
#     cat_x = [pos['x'] for pos in category_positions.values()]
#     cat_y = [pos['y'] for pos in category_positions.values()]
#     cat_names = list(category_positions.keys())
#     cat_colors_list = [category_colors[cat] for cat in cat_names]
    
#     # Determine text positions
#     text_positions = []
#     for n in nodes:
#         angle = n['angle']
#         if -np.pi/4 < angle < np.pi/4 or 3*np.pi/4 < angle < 5*np.pi/4:
#             text_positions.append('middle right' if np.cos(angle) > 0 else 'middle left')
#         else:
#             text_positions.append('top center' if np.sin(angle) > 0 else 'bottom center')
    
#     fig.add_trace(go.Scatter(
#         x=cat_x,
#         y=cat_y,
#         mode='markers+text',
#         marker=dict(
#             size=30,
#             color=cat_colors_list,
#             line=dict(color='black', width=2)
#         ),
#         text=cat_names,
#         textposition=text_positions,
#         textfont=dict(size=10, color='black', family='Arial Black'),
#         hovertemplate='<b>%{text}</b><extra></extra>',
#         showlegend=False,
#         name='Categories'
#     ))
    
#     # Add subcategory nodes (outer circle)
#     node_x = [n['x'] for n in nodes]
#     node_y = [n['y'] for n in nodes]
#     node_text = [f"{n['subcategory']}" for n in nodes]
#     # hover_text = [f"<b>{n['category']}</b><br>{n['subcategory']}<br>Count: {n['count']}" for n in nodes]
#     hover_text = [f"<b>{n['category']}</b><br>{n['subcategory']}" for n in nodes]
    
#     fig.add_trace(go.Scatter(
#         x=node_x,
#         y=node_y,
#         mode='markers+text',
#         marker=dict(
#             size=node_sizes,
#             color=node_colors,
#             line=dict(color='darkgray', width=2),
#             opacity=0.9
#         ),
#         text=node_text,
#         textposition=text_positions,
#         textfont=dict(size=8, color='black', family='Arial Black', shadow=True),
#         hovertemplate='%{hovertext}<extra></extra>',
#         hovertext=hover_text,
#         showlegend=True,
#         name='Subcategories'
#     ))
    
#     # Update layout
#     fig.update_layout(
#         title=dict(
#             text='Circular Dendrogram', # Title of the plot
#             x=0.5,
#             xanchor='center',
#             font=dict(size=24, color='#2c3e50', family='Arial Black', shadow=True)
#         ),
#         showlegend=False,
#         hovermode='closest',
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='white',
#         xaxis=dict(
#             showgrid=False,
#             zeroline=False,
#             showticklabels=False,
#             range=[-1.5, 1.5]
#         ),
#         yaxis=dict(
#             showgrid=False,
#             zeroline=False,
#             showticklabels=False,
#             range=[-1.5, 1.5]
#         ),
#         height=800,
#         margin=dict(t=40, b=20, l=20, r=20),
#         autosize=True
#     )
    
#     return fig


def create_circular_dendrogram(df, category_col, subcategory_col):
    
    tree_data = [{"name": "Flood Framework", "children": []}]
    
    # Color palette for categories
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
          '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']
    
    categories = df[category_col].unique()
    grouped = df.groupby([category_col, subcategory_col]).size().reset_index(name='count')
    
    for category in categories:
        cat_group = grouped[grouped[category_col] == category]
        children = []
        for _, row in cat_group.iterrows():
            children.append({
                "name": row[subcategory_col],
                "value": row['count'],
                "itemStyle": {"color": colors[hash(category) % len(colors)]}
            })

        tree_data[0]["children"].append({
            "name": category,
            "children": children,
            "itemStyle": {"color": colors[hash(category) % len(colors)]}
        })
    
        
    tree = (
        Tree(init_opts=opts.InitOpts(
            width="1200px", height="900px", renderer="canvas", bg_color="white"))
        .add(
            data=tree_data,
            collapse_interval=0,
            initial_tree_depth=-1,
            layout="radial",
            symbol="circle",
            symbol_size=15,
            orient="LR",
            series_name="Flood Framework",
            is_roam=True,
            label_opts=opts.LabelOpts(position="radial", rotate=0, vertical_align="middle")
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="Flood Risk Framework", ),
            tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, pos_left="right", feature={
                "saveAsImage": {},
                "restore": {},
                "dataView": {},
                "dataZoom": {},
            })
        )
    )
    return tree
            

def main():
    st.title("Flood Framework Circular Dendrogram")
    st.markdown("#### Visualize hierarchical flood risk data using a circular dendrogram.")
    
    dataCSV = DATA_DIR / "domains_subdomains_flourish(in).csv"
    
    if dataCSV is not None:
        # Read the CSV
        df = pd.read_csv(dataCSV)
        df.drop(columns="Count", inplace=True, errors='ignore')
        
        st.success(f"✅ Loaded {len(df)} rows")
        
        # Column selection
        col1, col2 = st.columns(2)
        
        with col1:
            category_col = st.selectbox(
                "Select Category Column (outer ring)",
                options=sorted(df.columns.tolist()),
                help="Main grouping level"
            )
            st.markdown(category_col)
        
        with col2:
            subcategory_col = st.selectbox(
                "Select Subcategory Column (inner ring)",
                options=[col for col in df.columns.tolist() if col != category_col],
                help="Sub-grouping level"
            )
        
        if category_col and subcategory_col:
            # Filtering section
            st.markdown("---")
            st.subheader("🎯 Filters")
            
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                st.markdown("**Filter by Category**")
                categories = df[category_col].unique().tolist()
                selected_categories = st.multiselect(
                    "Select categories to include",
                    options=categories,
                    default=categories,
                    key='category_filter'
                )
            
            # Filter dataframe by selected categories first
            filtered_df = df[df[category_col].isin(selected_categories)].copy()
            
            with filter_col2:
                st.markdown("**Filter by Subcategory**")
                subcategories = filtered_df[subcategory_col].unique().tolist()
                selected_subcategories = st.multiselect(
                    "Select subcategories to include",
                    options=subcategories,
                    default=subcategories,
                    key='subcategory_filter'
                )
            
            # Apply subcategory filter
            filtered_df = filtered_df[filtered_df[subcategory_col].isin(selected_subcategories)]
            
            # Display statistics
            st.markdown("---")
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.metric("Total Records", len(filtered_df))
            
            with metric_col2:
                st.metric("Categories", len(selected_categories))
            
            with metric_col3:
                st.metric("Subcategories", len(selected_subcategories))
            
            # Generate and display dendrogram
            if len(filtered_df) > 0:
                st.markdown("---")
                
                with st.spinner("Generating circular dendrogram..."):
                    fig = create_circular_dendrogram(
                        filtered_df,
                        category_col,
                        subcategory_col
                    )
                    
                    # st.plotly_chart(fig, width="stretch")
                    components.html(fig.render_embed(), height=900, scrolling=True)
                
                # Show filtered data
                with st.expander("📊 View Filtered Data"):
                    st.dataframe(filtered_df, width='stretch')
                    
                    # Download button for filtered data
                    csv_buffer = io.StringIO()
                    filtered_df.to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="⬇️ Download Filtered Data",
                        data=csv_buffer.getvalue(),
                        file_name="filtered_data.csv",
                        mime="text/csv"
                    )
            else:
                st.warning("⚠️ No data matches the current filters. Please adjust your selection.")
    
    else:
        # Landing page when no file is uploaded
        st.info("👆 Upload a CSV file using the sidebar to get started")
        
        st.markdown("### Sample CSV Format")
        st.markdown("""
        Your CSV should have at least two columns representing hierarchical levels:
        
        | Category | Subcategory | Value |
        |----------|-------------|-------|
        | Tech     | Software    | 100   |
        | Tech     | Hardware    | 150   |
        | Finance  | Banking     | 200   |
        | Finance  | Insurance   | 120   |
        """)

if __name__ == "__main__":
    main()
