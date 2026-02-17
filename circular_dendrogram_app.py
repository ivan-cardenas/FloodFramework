import streamlit as st
import pandas as pd
from pathlib import Path
# import plotly.graph_objects as go
from pyecharts import options as opts
from pyecharts.charts import Tree
from pyecharts.commons.utils import JsCode
import streamlit.components.v1 as components
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
import io

from pyecharts.globals import CurrentConfig

# Use jsDelivr CDN instead
CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@6.0.0/dist/"

THIS_DIR = Path(__file__).resolve().parent
DATA_DIR = THIS_DIR / "data"
LOGO_PATH = DATA_DIR / "Logo.png"
SECOND_LOGO_PATH = DATA_DIR / "logo_new_s4a.png"

# Page configuration
st.set_page_config(
    page_title="Flood vulnerability framework for deprived urban areas ",
    page_icon= "🌊",
    layout="wide"
)



# Custom CSS for better design
st.markdown("""
    <style>219ebc
    .main {
        padding: 2rem;
    }
    .stApp {
        background: #023047 0%
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

st.logo(LOGO_PATH, size="Large")


def create_circular_dendrogram(df, category_col, subcategory_col):
    
    tree_data = [{"name": "Flood Framework", "children": []}]
    
    # Color palette for categories
    colors = {
    "Social and demographic features": "#A6CEE3",
    "Sanitation and health infrastructure": "#1F78B4",
    "Spatial factors": "#B2DF8A",
    "Physical characteristics": "#33A02C",
    "Economic aspects": "#FB9A99",
    "Governance systems": "#E31A1C",
    "Institutional capacities": "#FDBF6F",
    "Community-led actions": "#FF7F00",
    "Awareness and alert systems": "#CAB2D6"
}
    
    domain_definitions = {
    "Social and demographic features": "Population composition, social roles, social capital, community dynamics, and demographic pressure that influence the vulnerability of individuals or groups, limiting their capacity to cope with and recover from floods.",
    "Sanitation and health infrastructure": "Infrastructure, services, and practices that safeguard community health before, during, and after flood crises—particularly sanitation provision and quality. ",
    "Spatial factors": "Influence of the location and distribution of people and structures in urban settlements, including placement of human activities and the morphology of built-up areas. ",
    "Physical characteristics": "Influence of the location and distribution of people and structures in urban settlements, including placement of human activities and the morphology of built-up areas. ",
    "Economic aspects": "Limiting or enabling economic conditions that either deepen or reduce flood vulnerability, including limitations in financial capacity, economic opportunity, and access to basic services and utilities. ",
    "Governance systems": "Systemic aspects that influence how decisions are made, implemented, and held accountable in flood risk management, including issues in planning, reinforcement, and trust. ",
    "Institutional capacities": "Factors that affect the ability of formal institutions to carry out disaster-related operations effectively, involving resources, skills, structure, and infrastructure. ",
    "Community-led actions": "Collective or individual practices initiated and carried out by community members themselves—without depending entirely on external agencies—to prevent and respond to flood impacts ",
    "Awareness and alert systems": "Knowledge and communication systems that inform and prepare residents. "
}
    
    categories = df[category_col].unique()
  
    grouped = df.groupby([category_col, subcategory_col, "explanation"]).size().reset_index(name='count')
  
    
    for i, category in enumerate(categories):
        cat_group = grouped[grouped[category_col] == category]
        color=colors.get(category, "#CCCCCC")  # Default color if category not in colors dict
        
        children = []
        for _, row in cat_group.iterrows():
            children.append({
                "name": row[subcategory_col],
                "value": row['count'],
                "itemStyle": {"color": color},
                "explanation" : row['explanation'],
            })
            

        tree_data[0]["children"].append({
            "name": category,
            "children": children,
            "itemStyle": {"color": color},
            "explanation" : domain_definitions.get(category, ""),
        })
        
    tree = (
        Tree(init_opts=opts.InitOpts(
            width="auto", height="900px", renderer="canvas", bg_color="white"))
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
            tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove",
                                          formatter=JsCode("""
                function(params) {
                    return '<b>' + params.name + '</b><br/>' +
                           '<i>' + params.data.explanation + '</i>';
                }
            """),
                                          extra_css_text="""
                                          display: flex; 
                                          flex-direction: column; 
                                          align-items: center; 
                                          max-width: 400px;
                                          white-space: normal;
                                          """),
            toolbox_opts=opts.ToolboxOpts(is_show=True, pos_left="right", feature={
                "saveAsImage": {"title": "Save as Image"},
                "restore": {"title": "Restore View"},
            })
        )
    )
    return tree
            

def main(): 
    
    logo, title = st.columns([1, 10])
    
    with logo:
        st.image(SECOND_LOGO_PATH, width=100)
    with title:
        st.title("Flood vulnerability framework for deprived urban areas ")
        st.markdown("### Co-developed with local stakeholders, tailored to African contexts.")
        st.markdown("""            
This platform shares a co-developed flood vulnerability framework designed for deprived urban areas in African cities. The framework supports city practitioners, community organizations and researchers in identifying locally relevant vulnerability mechanisms and translating them into context-sensitive flood assessments.  

The framework was co-developed through participatory workshops with community- and city-level stakeholders to map flood impacts and the vulnerability factors shaping them.  
                    
The definition of each domain and sub-domain can be found by hovering the mouse on top of them.  

In this platform you can either explore the domains and sub-domains emerged from the participatory approach, see their definition and typical mechanisms to flood impacts; or customize the framework to match your local context. Download of the tailored version is also possible. We encourage the use of the platform as facilitation tool in workshops with relevant local stakeholders, starting with the full generic framework, then collectively prioritize the most relevant domains, discussing connections between them.  
                    ---
                    """)
    
    dataCSV = DATA_DIR / "Domains_subDomains.csv"
    
    if dataCSV is not None:
        # Read the CSV
        df = pd.read_csv(dataCSV)
        df.drop(columns="Count", inplace=True, errors='ignore')
 
        
        # st.success(f"✅ Loaded {len(df)} rows")
        
        # Column selection
        col1, col2 = st.columns(2)
        
        with col1:
            category_col = st.selectbox(
                "Select Domain Column (Inner ring)",
                options=sorted(df.columns.tolist()),
                help="Main grouping level"
            )
        
        with col2:
            subcategory_col = st.selectbox(
                "Select Sub-Domain Column (Outer ring)",
                options=[col for col in df.columns.tolist() if col != category_col],
                help="Sub-grouping level"
            )
        
        if category_col and subcategory_col:
            # Filtering section
            st.markdown("---")
            st.subheader("🎯 Filters")
            
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                st.markdown("**Filter by Domain**")
                categories = df[category_col].unique().tolist()
                selected_categories = st.multiselect(
                    "Select domains to include",
                    options=categories,
                    default=categories,
                    key='category_filter'
                )
            
            # Filter dataframe by selected categories first
            filtered_df = df[df[category_col].isin(selected_categories)].copy()
            
            
            with filter_col2:
                st.markdown("**Filter by Sub-Domain**")
                subcategories = filtered_df[subcategory_col].unique().tolist()
                selected_subcategories = st.multiselect(
                    "Select sub-domains to include",
                    options=subcategories,
                    default=subcategories,
                    key='subcategory_filter'
                )
            
            # Apply subcategory filter
            filtered_df = filtered_df[filtered_df[subcategory_col].isin(selected_subcategories)]
            
            # # Display statistics
            # st.markdown("---")
            # metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            # with metric_col1:
            #     st.metric("Total Records", len(filtered_df))
            
            # with metric_col2:
            #     st.metric("Categories", len(selected_categories))
            
            # with metric_col3:
            #     st.metric("Subcategories", len(selected_subcategories))
            
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
        
        | Domain | Sub-Domain | Value |
        |----------|-------------|-------|
        | Tech     | Software    | 100   |
        | Tech     | Hardware    | 150   |
        | Finance  | Banking     | 200   |
        | Finance  | Insurance   | 120   |
        """)

    st.markdown("""
                ### Ethical Statement 

Workshop participation followed informed consent procedures and ethical approval from Geoethics Committee, application nr. 240127. We acknowledge the contributions of community participants and partner organizations who supported recruitment, facilitation, and contextual interpretation. 

**Study sites**: Nairobi, Kisumu (Kenya); Accra, Tema (Ghana); Beira, Chimoio (Mozambique). 

**Time period**: April 2024 - April 2025. 

**Local partners**: University of Ghana, SDI Kenya, Data4Moz.  

**Funding**: This research was carried out under the SPACE4ALL project (File number OCENW.M.21.168), funded by the Dutch Research Council (NWO).  


                
                """)
    
    st.markdown("""
                ## Authorship

The co-developed framework was created by the [SPACE4ALL](https://www.itc.nl/space4all/) research team, led by **Lorraine Trento Oliveira** [<img src="https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg" height="20"/>](https://www.linkedin.com/in/lorraine-t-oliveira/) [<img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" height="20"/>](https://orcid.org/0000-0002-2707-8006). The web platform was designed by **Iván Cárdenas León** [<img src="https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg" height="20"/>](https://www.linkedin.com/in/ivancardenasleon/) [<img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" height="20"/>](https://orcid.org/0009-0005-0245-633X).

**Contact**: [l.trentooliveira@utwente.nl](mailto:l.trentooliveira@utwente.nl)  
                """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()
