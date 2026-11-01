导入 streamlit 作为 st streamlit as st
import pandas as pd pandas as pd
导入 plotly.graph_objects 作为 go plotly.graph_objects as go
导入数学 math

# 设置页面
st.set_page_config(set_page_config(
    页面标题="固态储氢材料能量密度计算器""Solid-State Hydrogen Storage Material Energy Density Calculator",
    page_icon="🔋","🔋",
    布局="宽"，"wide",
    initial_sidebar_state="expanded""expanded"
)

# ==================== 自定义CSS样式 ====================
st.markdown("""        间隙: 2px;("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1f77b4;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2e86ab;
        margin: 1.5rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid #2e86ab;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    [data-testid="metric-container"] > div {
        background: transparent !important;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background: linear-gradient(135deg, #1f77b4 0%, #2e86ab 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stNumberInput input, .stTextInput input, .stSelectbox select {
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1f77b4 0%, #2e86ab 100%);
    }
    .stSuccess {
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 初始化session_state ====================
if 'initialized' not in st.session_state:
    # 材料参数
    st.session_state.material_option = "预设材料"
    st.session_state.selected_material = "MgH2"
    st.session_state.dehydrogenation_enthalpy = 76.1
    st.session_state.material_density = 1460
    st.session_state.hydrogen_mass_fraction = 0.0657

    # 燃料电池参数
    st.session_state.fuel_cell_efficiency = 60.0

    # 系统参数
    st.session_state.output_power = 30.0
    st.session_state.endurance_time = 5.0
    st.session_state.fuel_cell_mass = 26.0
    st.session_state.fuel_cell_volume = 14.2

    # 外壳参数
    st.session_state.container_shape = "圆柱"
    st.session_state.cylinder_input_mode = "按半径输入"
    st.session_state.container_radius = 0.2
    st.session_state.container_height_input = 0.5
    st.session_state.container_length = 0.4
    st.session_state.container_width = 0.3
    st.session_state.filling_ratio = 100.0
    st.session_state.container_thickness = 0.005
    st.session_state.container_count = 1

    # 自定义外壳参数（内部存储为m³）
    st.session_state.custom_shell_volume = 0.01          # 壳体材料体积 (m³)
    st.session_state.custom_internal_volume = 0.05       # 内部容积 (m³)

    # 外壳材料参数
    st.session_state.shell_material_option = "预设材料"
    st.session_state.selected_shell_material = "aluminum_6061"
    st.session_state.shell_density = 2700

    # 锂电池参数
    st.session_state.li_battery_mass_density = 0.30
    st.session_state.li_battery_volume_density = 500

    # 语言设置
    st.session_state.language = 'zh'

    # 自定义模式下的材料需求定义方式
    st.session_state.material_demand_mode = "按功率续航"

    st.session_state.initialized = True

# ==================== 多语言支持 ====================
TRANSLATIONS = {
    "zh": {
        "title": "🔋 固态储氢材料能量密度计算器",
        "subtitle": "基于脱氢能耗和燃料电池效率的固态储氢材料能量密度计算（考虑空间与续航稀释作用及外壳影响）",
        "sidebar_header": "计算参数设置",
        "material_selection": "材料选择",
        "material_option_preset": "预设材料",
        "material_option_custom": "自定义材料",
        "select_preset_material": "选择预设材料",
        "material_params": "材料参数",
        "dehydrogenation_enthalpy": "脱氢焓变",
        "material_density": "材料密度",
        "hydrogen_mass_fraction": "氢气质量分数",
        "custom_material_params": "自定义材料参数",
        "dehydrogenation_enthalpy_unit": "kJ/mol",
        "material_density_unit": "kg/m³",
        "fuel_cell_efficiency": "燃料电池效率",
        "fuel_cell_utilization": "燃料电池能量利用率",
        "exact_value": "精确值",
        "system_params": "系统参数",
        "output_power": "输出功率",
        "output_power_unit": "kW",
        "endurance_time": "续航时间",
        "endurance_time_unit": "h",
        "stack_mass": "电堆质量",
        "stack_mass_unit": "kg",
        "stack_volume": "电堆体积",
        "stack_volume_unit": "L",
        "shell_params": "外壳参数",
        "container_shape": "外壳形状",
        "cylinder": "圆柱",
        "cuboid": "长方体",
        "custom": "自定义",
        "cylinder_input_mode": "圆柱输入模式",
        "by_radius": "按半径输入",
        "by_height": "按高度输入",
        "minimum_surface": "最小表面积（最优形状）",
        "container_radius": "外壳半径",
        "container_height": "外壳高度",
        "container_length": "外壳长度",
        "container_width": "外壳宽度",
        "container_thickness": "外壳厚度",
        "container_count": "外壳数量",
        "container_count_unit": "个",
        "filling_ratio": "材料填充率",
        "mm_unit": "mm",
        "shell_material": "外壳材料",
        "shell_material_params": "外壳材料参数",
        "shell_density": "外壳材料密度",
        "li_battery_comparison": "锂电池对比参数",
        "li_battery_mass_density": "锂电池质量能量密度",
        "li_battery_volume_density": "锂电池体积能量密度",
        "kwh_kg": "kWh/kg",
        "kwh_m3": "kWh/m³",
        "current_material": "当前材料",
        "current_shell_material": "外壳材料",
        "current_fuel_cell_efficiency": "燃料电池效率",
        "current_container_shape": "外壳形状",
        "current_container_count": "外壳数量",
        "no_shell": "无外壳",
        "with_shell": "有外壳",
        "basic_calculation": "基础能量密度计算（不考虑系统稀释）",
        "system_calculation_no_shell": "系统能量密度计算（考虑空间与续航稀释，不含外壳）",
        "system_calculation_with_shell": "系统能量密度计算（罐装）",
        "endurance_comparison": "不同续航时间下的系统能量密度对比",
        "calculation_explanation": "计算说明",
        "material_comparison": "材料对比",
        "system_principle": "系统原理",
        "h2_energy_density": "氢气能量密度",
        "dehydrogenation_energy": "脱氢能耗",
        "fuel_cell_power": "燃料电池发电量",
        "net_power": "净产能",
        "mass_energy_density": "质量能量密度",
        "volume_energy_density": "体积能量密度",
        "system_requirements": "系统需求计算",
        "total_energy_required": "所需总能量",
        "material_mass_required": "所需材料质量",
        "material_volume_required": "所需材料体积",
        "system_total": "系统总成",
        "system_total_mass": "系统总质量",
        "system_total_volume": "系统总体积",
        "system_mass_energy_density": "系统质量能量密度",
        "system_volume_energy_density": "系统体积能量密度",
        "shell_status": "外壳状态",
        "shell_dimensions": "外壳尺寸",
        "single_shell_dimensions": "单个外壳尺寸",
        "total_shell_parameters": "外壳总参数",
        "single_shell_parameters": "单个外壳参数",
        "shell_parameters": "外壳参数",
        "shell_volume": "外壳体积",
        "shell_mass": "外壳质量",
        "total_shell_volume": "外壳总体积",
        "total_shell_mass": "外壳总质量",
        "single_shell_volume": "单个外壳体积",
        "single_shell_mass": "单个外壳质量",
        "material_per_container": "单个外壳内材料体积",
        "mass_energy_density_vs_time": "系统质量能量密度 - 续航时间",
        "volume_energy_density_vs_time": "系统体积能量密度 - 续航时间",
        "endurance_time_h": "续航时间 (h)",
        "mass_energy_density_unit": "质量能量密度 (kWh/kg)",
        "volume_energy_density_unit": "体积能量密度 (kWh/m³)",
        "basic_calculation_steps": "基础能量密度计算步骤",
        "dehydrogenation_calculation": "脱氢能耗计算",
        "fuel_cell_power_calculation": "燃料电池发电量计算",
        "net_power_calculation": "净产能计算",
        "material_energy_density_calculation": "材料能量密度计算",
        "shell_calculation_steps": "外壳计算步骤",
        "system_energy_density_steps": "系统能量密度计算步骤（含外壳）",
        "preset_hydrogen_materials": "预设储氢材料参数表",
        "preset_shell_materials": "预设外壳材料参数表",
        "material": "材料",
        "description": "描述",
        "key_concepts": "关键概念",
        "application_significance": "应用意义",
        "system_energy_density": "系统能量密度",
        "calculation_principle": "计算原理",
        "h2_mass_energy_density": "氢气质量能量密度",
        "li_battery_reference": "锂电池参考值",
        "fixed_value": "固定值",
        "help_material_selection": "选择预设材料或自定义材料参数",
        "help_preset_material": "从预设材料库中选择",
        "help_dehydrogenation_enthalpy": "脱氢反应的焓变值",
        "help_material_density": "储氢材料的密度",
        "help_hydrogen_mass_fraction": "储氢材料中氢气的质量分数",
        "help_fuel_cell_efficiency": "使用按钮调整燃料电池能量利用率",
        "help_exact_value": "精确输入燃料电池能量利用率",
        "help_output_power": "燃料电池系统的输出功率",
        "help_endurance_time": "系统续航时间",
        "help_stack_mass": "燃料电池电堆的质量",
        "help_stack_volume": "燃料电池电堆的体积",
        "help_container_shape": "选择储氢容器的形状",
        "help_cylinder_input": "选择圆柱的输入方式",
        "help_container_radius": "圆柱形容器的半径",
        "help_container_height": "圆柱形容器的高度",
        "help_container_length": "长方体容器的长度",
        "help_container_width": "长方体容器的宽度",
        "help_container_thickness": "外壳的厚度，设为0表示无外壳",
        "help_container_count": "储氢罐的数量，将材料需求量均分到每个罐子中",
        "help_filling_ratio": "外壳内材料填充的百分比，考虑颗粒间隙和实际填充情况",
        "help_shell_material": "选择预设外壳材料或自定义材料密度",
        "help_preset_shell_material": "从预设外壳材料库中选择",
        "help_shell_density": "外壳材料的密度",
        "help_li_battery_mass": "传统锂电池的质量能量密度",
        "help_li_battery_volume": "传统锂电池的体积能量密度",
        "base_area": "底面积",
        "outer_volume": "外体积",
        "inner_radius": "内半径",
        "inner_base_area": "内底面积",
        "inner_height": "内高度",
        "inner_volume": "内体积",
        "inner_length": "内长度",
        "inner_width": "内宽度",
        "material_requirements": "材料需求计算",
        "calculation": "计算",
        "consider_only_the_energy_density_of_the_hydrogen_storage_material_itself": "仅考虑储氢材料本身的能量密度",
        "actual_energy_density_after_considering_fuel_cell_system_mass_and_volume": "考虑燃料电池系统质量和体积后的实际能量密度",
        "actual_energy_density_further_considering_shell_mass_and_volume": "进一步考虑外壳质量和体积后的实际能量密度",
        "dilution_effect": "稀释作用",
        "as_endurance_time_increases_system_energy_density_approaches_material_energy_density": "随着续航时间增加，系统能量密度趋近于材料能量密度",
        "short_endurance_applications": "短续航应用",
        "system_energy_density_is_greatly_affected_by_stack_and_shell": "系统能量密度受电堆和外壳影响较大",
        "long_endurance_applications": "长续航应用",
        "system_energy_density_approaches_material_energy_density": "系统能量密度趋近于材料能量密度",
        "system_design": "系统设计",
        "balance_between_endurance_requirements_system_compactness_and_shell_design": "需要在续航需求、系统紧凑性和外壳设计之间平衡",
        "solid_state_hydrogen_storage_material_energy_density_calculation_based_on_dehydrogenation_energy_consumption_fuel_cell_efficiency_system_parameters_and_shell_parameters": "基于脱氢能耗、燃料电池效率、系统参数和外壳参数的固态储氢材料能量密度计算",
        "internal_volume_required": "所需内部容积",
        "filling_ratio_calculation": "填充率计算",
        "results_tab": "📈 计算结果",
        "comparison_tab": "📊 性能对比",
        "explanation_tab": "🔍 计算说明",
        "materials_tab": "📋 材料库",
        "principle_tab": "📚 系统原理",
        "material_params_expander": "🔬 材料参数",
        "fuel_cell_params_expander": "⚡ 燃料电池参数",
        "system_params_expander": "🔧 系统参数",
        "shell_params_expander": "📦 外壳参数",
        "battery_params_expander": "🔋 锂电池参数",
        "calculation_complete": "✅ 计算完成！所有结果已更新。",
        "energy_density_dilution_sankey": "📉 能量密度稀释过程桑基图",
        "energy_density_dilution_description": "展示从理论材料能量密度到实际系统能量密度的逐步稀释过程",
        "hydrogen_chemical_energy": "氢气化学能",
        "dehydrogenation_energy_loss": "脱氢能耗损失",
        "remaining_chemical_energy": "剩余化学能",
        "fuel_cell_efficiency_loss": "燃料电池效率损失",
        "material_energy_density": "材料能量密度",
        "stack_dilution_effect": "电堆稀释效应",
        "system_energy_density_no_shell": "系统能量密度（无外壳）",
        "shell_dilution_effect": "外壳稀释效应",
        "final_system_energy_density": "最终系统能量密度",
        "dilution_process": "稀释过程",
        "energy_density_flow": "能量密度流",
        "sankey_diagram_explanation": "桑基图说明",
        "sankey_explanation_text": "此桑基图展示了能量密度从理论材料值到实际系统值的逐步稀释过程。箭头宽度代表能量密度值的大小，清晰显示了在脱氢能耗、燃料电池效率损失、电堆质量和外壳质量等因素影响下能量密度的逐步降低。质量能量密度和体积能量密度的稀释过程结构相同，仅数值不同。",
        "key_observations": "关键观察",
        "observation_1": "脱氢能耗对能量密度的影响",
        "observation_2": "燃料电池效率损失的影响",
        "observation_3": "电堆质量对能量密度的稀释效应",
        "observation_4": "外壳质量进一步降低系统能量密度",
        "observation_5": "最终系统能量密度相比材料能量密度的保留比例",
        "dilution_ratio": "稀释比例",
        "dehydrogenation_impact": "脱氢能耗影响",
        "fuel_cell_impact": "燃料电池效率影响",
        "stack_mass_impact": "电堆质量影响",
        "shell_mass_impact": "外壳质量影响",
        "total_dilution": "总稀释",
        "both_dilution_processes": "两种能量密度的稀释过程结构相同",
        "minimum_surface_info1": "系统将自动计算直径等于高度的最优尺寸",
        "minimum_surface_info2": "圆柱体直径等于高度时具有最小表面积（最优形状）",
        "batch_export": "📊 批量计算与导出",
        "batch_settings": "批量计算设置",
        "efficiency_range": "燃料电池效率范围",
        "start_efficiency": "起始效率 (%)",
        "end_efficiency": "结束效率 (%)",
        "step_efficiency": "步长 (%)",
        "select_shell_materials": "选择要计算的外壳材料",
        "start_batch": "开始批量计算",
        "batch_results": "批量计算结果",
        "download_csv": "下载结果 CSV",
        "shell_material_name": "外壳材料",
        "efficiency": "燃料电池效率 (%)",
        "mass_energy_density_system": "系统质量能量密度 (kWh/kg)",
        "volume_energy_density_system": "系统体积能量密度 (kWh/m³)",
        "total_system_mass_batch": "系统总质量 (kg)",
        "total_system_volume_batch": "系统总体积 (L)",
        "select_hydrogen_materials": "选择要计算的储氢材料",
        "hydrogen_material_name": "储氢材料",
        "filling_ratio_range": "材料填充率范围",
        "start_filling_ratio": "起始填充率 (%)",
        "end_filling_ratio": "结束填充率 (%)",
        "step_filling_ratio": "步长 (%)",
        "shape_configuration": "外壳形状配置",
        "enable_shape": "启用此形状",
        "shape_cylinder_radius": "圆柱（按半径）",
        "shape_cylinder_height": "圆柱（按高度）",
        "shape_cylinder_optimal": "圆柱（最小表面积）",
        "shape_cuboid": "长方体",
        "shape_radius_mm": "半径 (mm)",
        "shape_height_mm": "高度 (mm)",
        "shape_length_mm": "长度 (mm)",
        "shape_width_mm": "宽度 (mm)",
        "fuel_cell_presets": "燃料电池预设",
        "select_fuel_cell_presets": "选择燃料电池型号（不选则使用侧边栏值）",
        "fuel_cell_model": "燃料电池型号 (kW/kg/L)",
        "endurance_time_range": "续航时间范围",
        "start_endurance": "起始续航时间 (h)",
        "end_endurance": "结束续航时间 (h)",
        "step_endurance": "步长 (h)",
        "endurance_h": "续航时间 (h)",
        "shell_dimensions_table": "外壳尺寸统计表",
        "shape_radius_m": "半径 (m)",
        "shape_height_m": "高度 (m)",
        "shape_length_m": "长度 (m)",
        "shape_width_m": "宽度 (m)",
        "download_dimensions_csv": "下载尺寸统计 CSV",
        "custom_shell_mass": "外壳壳体体积",
        "custom_shell_volume": "外壳总体积（计算值）",
        "custom_shape_note": "输入壳体体积、内部容积和填充率，材料体积 = 内部容积 × 填充率",
        "custom_shell_mass_unit": "L",
        "custom_shell_volume_unit": "L",
        "material_demand_mode": "材料需求定义方式",
        "mode_power": "按功率续航",
        "mode_volume": "按外壳容积",
        "custom_internal_volume": "外壳内部容积",
        "custom_internal_volume_unit": "L",
        "custom_internal_note": "内部空腔体积（未填充材料部分）"
    },
    "en": {
        "title": "🔋 Solid-State Hydrogen Storage Material Energy Density Calculator",
        "subtitle": "Energy density calculation for solid-state hydrogen storage materials based on dehydrogenation energy and fuel cell efficiency (considering space and endurance dilution effects and shell influence)",
        "sidebar_header": "Parameter Settings",
        "material_selection": "Material Selection",
        "material_option_preset": "Preset Materials",
        "material_option_custom": "Custom Materials",
        "select_preset_material": "Select Preset Material",
        "material_params": "Material Parameters",
        "dehydrogenation_enthalpy": "Dehydrogenation Enthalpy",
        "material_density": "Material Density",
        "hydrogen_mass_fraction": "Hydrogen Mass Fraction",
        "custom_material_params": "Custom Material Parameters",
        "dehydrogenation_enthalpy_unit": "kJ/mol",
        "material_density_unit": "kg/m³",
        "fuel_cell_efficiency": "Fuel Cell Efficiency",
        "fuel_cell_utilization": "Fuel Cell Energy Utilization",
        "exact_value": "Exact Value",
        "system_params": "System Parameters",
        "output_power": "Output Power",
        "output_power_unit": "kW",
        "endurance_time": "Endurance Time",
        "endurance_time_unit": "h",
        "stack_mass": "Stack Mass",
        "stack_mass_unit": "kg",
        "stack_volume": "Stack Volume",
        "stack_volume_unit": "L",
        "shell_params": "Shell Parameters",
        "container_shape": "Container Shape",
        "cylinder": "Cylinder",
        "cuboid": "Cuboid",
        "custom": "Custom",
        "cylinder_input_mode": "Cylinder Input Mode",
        "by_radius": "By Radius",
        "by_height": "By Height",
        "minimum_surface": "Minimum Surface (Optimal Shape)",
        "container_radius": "Container Radius",
        "container_height": "Container Height",
        "container_length": "Container Length",
        "container_width": "Container Width",
        "container_thickness": "Container Thickness",
        "container_count": "Number of Containers",
        "container_count_unit": "pcs",
        "filling_ratio": "Material Filling Ratio",
        "mm_unit": "mm",
        "shell_material": "Shell Material",
        "shell_material_params": "Shell Material Parameters",
        "shell_density": "Shell Material Density",
        "li_battery_comparison": "Lithium Battery Parameters",
        "li_battery_mass_density": "Li Battery Mass Energy Density",
        "li_battery_volume_density": "Li Battery Volume Energy Density",
        "kwh_kg": "kWh/kg",
        "kwh_m3": "kWh/m³",
        "current_material": "Current Material",
        "current_shell_material": "Shell Material",
        "current_fuel_cell_efficiency": "Fuel Cell Efficiency",
        "current_container_shape": "Container Shape",
        "current_container_count": "Number of Containers",
        "no_shell": "No Shell",
        "with_shell": "With Shell",
        "basic_calculation": "Basic Energy Density (Without System Dilution)",
        "system_calculation_no_shell": "System Energy Density (With space and battery life dilution, excluding the outer shell)",
        "system_calculation_with_shell": "System Energy Density (Containerized)",
        "endurance_comparison": "System Energy Density vs Endurance Time",
        "calculation_explanation": "Calculation Details",
        "material_comparison": "Material Comparison",
        "system_principle": "System Principle",
        "h2_energy_density": "Hydrogen Energy Density",
        "dehydrogenation_energy": "Dehydrogenation Energy",
        "fuel_cell_power": "Fuel Cell Power Output",
        "net_power": "Net Power Output",
        "mass_energy_density": "Mass Energy Density",
        "volume_energy_density": "Volume Energy Density",
        "system_requirements": "System Requirements",
        "total_energy_required": "Total Energy Required",
        "material_mass_required": "Material Mass Required",
        "material_volume_required": "Material Volume Required",
        "system_total": "System Total",
        "system_total_mass": "System Total Mass",
        "system_total_volume": "System Total Volume",
        "system_mass_energy_density": "System Mass Energy Density",
        "system_volume_energy_density": "System Volume Energy Density",
        "shell_status": "Shell Status",
        "shell_dimensions": "Shell Dimensions",
        "single_shell_dimensions": "Single Shell Dimensions",
        "total_shell_parameters": "Total Shell Parameters",
        "single_shell_parameters": "Single Shell Parameters",
        "shell_parameters": "Shell Parameters",
        "shell_volume": "Shell Volume",
        "shell_mass": "Shell Mass",
        "total_shell_volume": "Total Shell Volume",
        "total_shell_mass": "Total Shell Mass",
        "single_shell_volume": "Single Shell Volume",
        "single_shell_mass": "Single Shell Mass",
        "material_per_container": "Material Volume per Container",
        "mass_energy_density_vs_time": "System Mass Energy Density vs Endurance Time",
        "volume_energy_density_vs_time": "System Volume Energy Density vs Endurance Time",
        "endurance_time_h": "Endurance Time (h)",
        "mass_energy_density_unit": "Mass Energy Density (kWh/kg)",
        "volume_energy_density_unit": "Volume Energy Density (kWh/m³)",
        "basic_calculation_steps": "Basic Energy Density Calculation Steps",
        "dehydrogenation_calculation": "Dehydrogenation Energy Calculation",
        "fuel_cell_power_calculation": "Fuel Cell Power Output Calculation",
        "net_power_calculation": "Net Power Output Calculation",
        "material_energy_density_calculation": "Material Energy Density Calculation",
        "shell_calculation_steps": "Shell Calculation Steps",
        "system_energy_density_steps": "System Energy Density Calculation Steps (With Shell)",
        "preset_hydrogen_materials": "Preset Hydrogen Storage Materials",
        "preset_shell_materials": "Preset Shell Materials",
        "material": "Material",
        "description": "Description",
        "key_concepts": "Key Concepts",
        "application_significance": "Application Significance",
        "calculation_principle": "Calculation Principle",
        "h2_mass_energy_density": "Hydrogen Mass Energy Density",
        "li_battery_reference": "Lithium Battery Reference Values",
        "fixed_value": "Fixed Value",
        "help_material_selection": "Select preset materials or custom material parameters",
        "help_preset_material": "Select from preset material library",
        "help_dehydrogenation_enthalpy": "Enthalpy change of dehydrogenation reaction",
        "help_material_density": "Density of hydrogen storage material",
        "help_hydrogen_mass_fraction": "Mass fraction of hydrogen in the storage material",
        "help_fuel_cell_efficiency": "Adjust fuel cell energy utilization rate using slider",
        "help_exact_value": "Precisely input fuel cell energy utilization rate",
        "help_output_power": "Output power of fuel cell system",
        "help_endurance_time": "System endurance time",
        "help_stack_mass": "Mass of fuel cell stack",
        "help_stack_volume": "Volume of fuel cell stack",
        "help_container_shape": "Select the shape of hydrogen storage container",
        "help_cylinder_input": "Select cylinder input method",
        "help_container_radius": "Radius of cylindrical container",
        "help_container_height": "Height of cylindrical container",
        "help_container_length": "Length of cuboid container",
        "help_container_width": "Width of cuboid container",
        "help_container_thickness": "Shell thickness, set to 0 for no shell",
        "help_container_count": "Number of hydrogen storage containers, material requirement will be evenly distributed to each container",
        "help_filling_ratio": "Percentage of material filling inside the shell, considering particle gaps and actual filling",
        "help_shell_material": "Select preset shell material or custom material density",
        "help_preset_shell_material": "Select from preset shell material library",
        "help_shell_density": "Density of shell material",
        "help_li_battery_mass": "Mass energy density of traditional lithium battery",
        "help_li_battery_volume": "Volume energy density of traditional lithium battery",
        "base_area": "Base Area",
        "outer_volume": "Outer Volume",
        "inner_radius": "Inner Radius",
        "inner_base_area": "Inner Base Area",
        "inner_height": "Inner Height",
        "inner_volume": "Inner Volume",
        "inner_length": "Inner Length",
        "inner_width": "Inner Width",
        "material_requirements": "Material Requirements Calculation",
        "calculation": "Calculation",
        "consider_only_the_energy_density_of_the_hydrogen_storage_material_itself": "Consider only the energy density of the hydrogen storage material itself",
        "actual_energy_density_after_considering_fuel_cell_system_mass_and_volume": "Actual energy density after considering fuel cell system mass and volume",
        "actual_energy_density_further_considering_shell_mass_and_volume": "Actual energy density further considering shell mass and volume",
        "dilution_effect": "Dilution Effect",
        "as_endurance_time_increases_system_energy_density_approaches_material_energy_density": "As endurance time increases, system energy density approaches material energy density",
        "short_endurance_applications": "Short Endurance Applications",
        "system_energy_density_is_greatly_affected_by_stack_and_shell": "System energy density is greatly affected by stack and shell",
        "long_endurance_applications": "Long Endurance Applications",
        "system_energy_density_approaches_material_energy_density": "System energy density approaches material energy density",
        "system_design": "System Design",
        "balance_between_endurance_requirements_system_compactness_and_shell_design": "Balance between endurance requirements, system compactness and shell design",
        "solid_state_hydrogen_storage_material_energy_density_calculation_based_on_dehydrogenation_energy_consumption_fuel_cell_efficiency_system_parameters_and_shell_parameters": "Solid-state hydrogen storage material energy density calculation based on dehydrogenation energy, fuel cell efficiency, system parameters and shell parameters",
        "internal_volume_required": "Required Internal Volume",
        "filling_ratio_calculation": "Filling Ratio Calculation",
        "results_tab": "📈 Results",
        "comparison_tab": "📊 Performance",
        "explanation_tab": "🔍 Calculation",
        "materials_tab": "📋 Materials",
        "principle_tab": "📚 Principle",
        "material_params_expander": "🔬 Materials",
        "fuel_cell_params_expander": "⚡ Fuel Cell",
        "system_params_expander": "🔧 System",
        "shell_params_expander": "📦 Shell",
        "battery_params_expander": "🔋 Battery",
        "calculation_complete": "✅ Calculation completed! All results updated.",
        "energy_density_dilution_sankey": "📉 Energy Density Dilution Sankey Diagram",
        "energy_density_dilution_description": "Showing the step-by-step dilution process from theoretical material energy density to actual system energy density",
        "hydrogen_chemical_energy": "Hydrogen Chemical Energy",
        "dehydrogenation_energy_loss": "Dehydrogenation Energy Loss",
        "remaining_chemical_energy": "Remaining Chemical Energy",
        "fuel_cell_efficiency_loss": "Fuel Cell Efficiency Loss",
        "material_energy_density": "Material Energy Density",
        "stack_dilution_effect": "Stack Dilution Effect",
        "system_energy_density_no_shell": "System Energy Density (No Shell)",
        "shell_dilution_effect": "Shell Dilution Effect",
        "final_system_energy_density": "Final System Energy Density",
        "dilution_process": "Dilution Process",
        "energy_density_flow": "Energy Density Flow",
        "sankey_diagram_explanation": "Sankey Diagram Explanation",
        "sankey_explanation_text": "This Sankey diagram shows the step-by-step dilution of energy density from theoretical material values to actual system values. Arrow widths represent the magnitude of energy density values, clearly showing the reduction in energy density due to dehydrogenation energy consumption, fuel cell efficiency loss, stack mass, and shell mass. The dilution process structure is identical for both mass and volume energy densities, with only numerical values differing.",
        "key_observations": "Key Observations",
        "observation_1": "Impact of dehydrogenation energy on energy density",
        "observation_2": "Impact of fuel cell efficiency loss",
        "observation_3": "Dilution effect of stack mass on energy density",
        "observation_4": "Further reduction of system energy density by shell mass",
        "observation_5": "Retention ratio of final system energy density compared to material energy density",
        "dilution_ratio": "Dilution Ratio",
        "dehydrogenation_impact": "Dehydrogenation Impact",
        "fuel_cell_impact": "Fuel Cell Impact",
        "stack_mass_impact": "Stack Mass Impact",
        "shell_mass_impact": "Shell Mass Impact",
        "total_dilution": "Total Dilution",
        "both_dilution_processes": "Both energy density dilution processes share identical structure",
        "minimum_surface_info1": "The system will automatically calculate the optimal dimensions where diameter equals height",
        "minimum_surface_info2": "Cylinder with diameter equal to height has minimum surface area (Optimal shape)",
        "batch_export": "📊 Batch Export",
        "batch_settings": "Batch Calculation Settings",
        "efficiency_range": "Fuel Cell Efficiency Range",
        "start_efficiency": "Start Efficiency (%)",
        "end_efficiency": "End Efficiency (%)",
        "step_efficiency": "Step (%)",
        "select_shell_materials": "Select Shell Materials",
        "start_batch": "Run Batch Calculation",
        "batch_results": "Batch Results",
        "download_csv": "Download CSV",
        "shell_material_name": "Shell Material",
        "efficiency": "Fuel Cell Efficiency (%)",
        "mass_energy_density_system": "System Mass Energy Density (kWh/kg)",
        "volume_energy_density_system": "System Volume Energy Density (kWh/m³)",
        "total_system_mass_batch": "Total System Mass (kg)",
        "total_system_volume_batch": "Total System Volume (L)",
        "select_hydrogen_materials": "Select Hydrogen Storage Materials",
        "hydrogen_material_name": "H₂ Storage Material",
        "shape_configuration": "Shell Shape Configuration",
        "enable_shape": "Enable this shape",
        "shape_cylinder_radius": "Cylinder (by radius)",
        "shape_cylinder_height": "Cylinder (by height)",
        "shape_cylinder_optimal": "Cylinder (optimal)",
        "shape_cuboid": "Cuboid",
        "shape_radius_mm": "Radius (mm)",
        "shape_height_mm": "Height (mm)",
        "shape_length_mm": "Length (mm)",
        "shape_width_mm": "Width (mm)",
        "filling_ratio_range": "Filling Ratio Range",
        "start_filling_ratio": "Start Filling Ratio (%)",
        "end_filling_ratio": "End Filling Ratio (%)",
        "step_filling_ratio": "Step (%)",
        "fuel_cell_presets": "Fuel Cell Presets",
        "select_fuel_cell_presets": "Select fuel cell models (if none selected, use sidebar values)",
        "fuel_cell_model": "Fuel Cell Model (kW/kg/L)",
        "endurance_time_range": "Endurance Time Range",
        "start_endurance": "Start Endurance (h)",
        "end_endurance": "End Endurance (h)",
        "step_endurance": "Step (h)",
        "endurance_h": "Endurance (h)",
        "shell_dimensions_table": "Shell Dimensions Summary",
        "shape_radius_m": "Radius (m)",
        "shape_height_m": "Height (m)",
        "shape_length_m": "Length (m)",
        "shape_width_m": "Width (m)",
        "download_dimensions_csv": "Download Dimensions CSV",
        "custom_shell_mass": "Shell Solid Volume",
        "custom_shell_volume": "Shell Total Volume (calc)",
        "custom_shape_note": "Input solid volume, internal volume and filling ratio, material volume = internal volume × filling ratio",
        "custom_shell_mass_unit": "L",
        "custom_shell_volume_unit": "L",
        "material_demand_mode": "Material Demand Definition",
        "mode_power": "By Power & Endurance",
        "mode_volume": "By Shell Volume",
        "custom_internal_volume": "Internal Cavity Volume",
        "custom_internal_volume_unit": "L",
        "custom_internal_note": "Empty internal volume (unfilled space)"
    }
}

def t(key):
    return TRANSLATIONS[st.session_state.language].get(key, key)

# 语言选择器
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    language = st.selectbox(
        "🌐 Language / 语言",
        options=["zh", "en"],
        format_func=lambda x: "简体中文" if x == "zh" else "English",
        key="language_selector"
    )
    if language != st.session_state.language:
        st.session_state.language = language

# ==================== 预设材料数据库 ====================
PRESET_MATERIALS = {
    "MgH2": {
        "dehydrogenation_enthalpy": 76.1,
        "material_density": 1460,
        "hydrogen_mass_fraction": 0.0657,
        "description": {"zh": "氢化镁 - 常见固态储氢材料", "en": "Magnesium Hydride - Common solid-state hydrogen storage material"}
    },
    "TiFeH2": {
        "dehydrogenation_enthalpy": 27.4,
        "material_density": 5420,
        "hydrogen_mass_fraction": 0.0079,
        "description": {"zh": "钛铁氢化物 - 低脱氢温度", "en": "Titanium Iron Hydride - Low dehydrogenation temperature"}
    },
    "Mg2NiH4": {
        "dehydrogenation_enthalpy": 67.0,
        "material_density": 2780,
        "hydrogen_mass_fraction": 0.033,
        "description": {"zh": "镁镍氢化物 - 中等储氢密度", "en": "Magnesium Nickel Hydride - Medium hydrogen storage density"}
    },
    "LaNi5H6": {
        "dehydrogenation_enthalpy": 34.09,
        "material_density": 7120,
        "hydrogen_mass_fraction": 0.0159,
        "description": {"zh": "镧镍氢化物 - 优良循环性能", "en": "Lanthanum Nickel Hydride - Excellent cycle performance"}
    },
    "LiAlH4": {
        "dehydrogenation_enthalpy": 36.3,
        "material_density": 910,
        "hydrogen_mass_fraction": 0.106,
        "description": {"zh": "氢化铝锂 - 高储氢密度", "en": "Lithium Aluminum Hydride - High hydrogen storage density (irreversible)"}
    },
    "NaBH4": {
        "dehydrogenation_enthalpy": 108.0,
        "material_density": 1080,
        "hydrogen_mass_fraction": 0.106,
        "description": {"zh": "硼氢化钠 - 高储氢密度", "en": "Sodium Borohydride - High hydrogen storage density (irreversible)"}
    }
}

PRESET_SHELL_MATERIALS = {
    "aluminum_6061": {
        "display_name": {"zh": "铝合金6061-T6", "en": "Aluminum 6061-T6"},
        "density": 2700,
        "description": {"zh": "铝合金6061-T6 - 轻质、良好的强度和耐腐蚀性", "en": "Aluminum Alloy 6061-T6 - Lightweight, good strength and corrosion resistance"}
    },
    "stainless_steel_304": {
        "display_name": {"zh": "不锈钢304", "en": "Stainless Steel 304"},
        "density": 8000,
        "description": {"zh": "不锈钢304 - 良好的耐腐蚀性和机械性能", "en": "Stainless Steel 304 - Good corrosion resistance and mechanical properties"}
    },
    "titanium_alloy": {
        "display_name": {"zh": "钛合金Ti-6Al-4V", "en": "Titanium Alloy Ti-6Al-4V"},
        "density": 4430,
        "description": {"zh": "钛合金Ti-6Al-4V - 高强度、轻质、耐高温", "en": "Titanium Alloy Ti-6Al-4V - High strength, lightweight, high temperature resistance"}
    },
    "inconel_600": {
        "display_name": {"zh": "高密度聚乙烯 (HDPE)", "en": "Polyethylene (HDPE)"},
        "density": 952,
        "description": {"zh": "高密度聚乙烯 (HDPE) - 兼具密封和部分承压", "en": "Polyethylene (HDPE) - Partially sealed with local pressure resistance"}
    },
    "hastelloy_c276": {
        "display_name": {"zh": "环氧树脂复合材料", "en": "E-glass/Epoxy Composite"},
        "density": 1900,
        "description": {"zh": "环氧树脂复合材料 - 极佳的耐腐蚀性和中等强度", "en": "E-glass/Epoxy Composite - Excellent corrosion resistance and medium high strength"}
    },
    "tantalum": {
        "display_name": {"zh": "316L 奥氏体不锈钢", "en": "316L Austenitic Stainless Steel"},
        "density": 7920,
        "description": {"zh": "316L 奥氏体不锈钢 - 良好的耐腐蚀性和机械性能", "en": "316L Austenitic Stainless Steel - Extremely high corrosion resistance, excellent high temperature performance"}
    }
}

H2_ENERGY_DENSITY = 39.4  # kWh/kg
LI_BATTERY_MASS_DENSITY = 0.30
LI_BATTERY_VOLUME_DENSITY = 500

st.markdown(f'<h1 class="main-header">{t("title")}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">{t("subtitle")}</p>', unsafe_allow_html=True)

# 侧边栏输入
st.sidebar.header(t("sidebar_header"))

with st.sidebar.expander(t("material_params_expander"), expanded=True):
    material_option = st.radio(t("material_selection"), [t("material_option_preset"), t("material_option_custom")], help=t("help_material_selection"), key="material_option_input")
    st.session_state.material_option = material_option
    if material_option == t("material_option_preset"):
        selected_material = st.selectbox(t("select_preset_material"), list(PRESET_MATERIALS.keys()), format_func=lambda x: f"{x} - {PRESET_MATERIALS[x]['description'][st.session_state.language]}", help=t("help_preset_material"), key="selected_material_input")
        st.session_state.selected_material = selected_material
        material_data = PRESET_MATERIALS[selected_material]
        dehydrogenation_enthalpy = material_data["dehydrogenation_enthalpy"]
        material_density = material_data["material_density"]
        hydrogen_mass_fraction = material_data["hydrogen_mass_fraction"]
        st.session_state.dehydrogenation_enthalpy = dehydrogenation_enthalpy
        st.session_state.material_density = material_density
        st.session_state.hydrogen_mass_fraction = hydrogen_mass_fraction
        st.markdown(f"**{t('material_params')}**")
        st.text(f"{t('dehydrogenation_enthalpy')}: {dehydrogenation_enthalpy} {t('dehydrogenation_enthalpy_unit')}")
        st.text(f"{t('material_density')}: {material_density} {t('material_density_unit')}")
        st.text(f"{t('hydrogen_mass_fraction')}: {hydrogen_mass_fraction:.3f}")
    else:
        st.subheader(t("custom_material_params"))
        dehydrogenation_enthalpy = st.number_input(f"{t('dehydrogenation_enthalpy')} ({t('dehydrogenation_enthalpy_unit')})", min_value=0.0, value=float(st.session_state.dehydrogenation_enthalpy), step=0.1, help=t("help_dehydrogenation_enthalpy"), key="custom_dehydrogenation_enthalpy_input")
        st.session_state.dehydrogenation_enthalpy = dehydrogenation_enthalpy
        material_density = st.number_input(f"{t('material_density')} ({t('material_density_unit')})", min_value=0, value=st.session_state.material_density, step=10, help=t("help_material_density"), key="custom_material_density_input")
        st.session_state.material_density = material_density
        hydrogen_mass_fraction = st.number_input(t("hydrogen_mass_fraction"), min_value=0.0, max_value=1.0, value=st.session_state.hydrogen_mass_fraction, step=0.001, help=t("help_hydrogen_mass_fraction"), format="%.3f", key="custom_hydrogen_mass_fraction_input")
        st.session_state.hydrogen_mass_fraction = hydrogen_mass_fraction

with st.sidebar.expander(t("fuel_cell_params_expander"), expanded=True):
    fuel_cell_efficiency = st.number_input(f"{t('fuel_cell_efficiency')} (%)", min_value=0.0, max_value=100.0, value=st.session_state.fuel_cell_efficiency, step=5.0, format="%.1f", help=t("help_fuel_cell_efficiency"), key="fuel_cell_efficiency_input")
    st.session_state.fuel_cell_efficiency = fuel_cell_efficiency

with st.sidebar.expander(t("system_params_expander"), expanded=True):
    output_power = st.number_input(f"{t('output_power')} ({t('output_power_unit')})", min_value=0.0, value=st.session_state.output_power, step=5.0, help=t("help_output_power"), key="output_power_input")
    st.session_state.output_power = output_power
    endurance_time = st.number_input(f"{t('endurance_time')} ({t('endurance_time_unit')})", min_value=0.0, value=st.session_state.endurance_time, step=0.5, help=t("help_endurance_time"), key="endurance_time_input")
    st.session_state.endurance_time = endurance_time
    fuel_cell_mass = st.number_input(f"{t('stack_mass')} ({t('stack_mass_unit')})", min_value=0.0, value=st.session_state.fuel_cell_mass, step=1.0, help=t("help_stack_mass"), key="fuel_cell_mass_input")
    st.session_state.fuel_cell_mass = fuel_cell_mass
    fuel_cell_volume = st.number_input(f"{t('stack_volume')} ({t('stack_volume_unit')})", min_value=0.0, value=st.session_state.fuel_cell_volume, step=0.1, help=t("help_stack_volume"), key="fuel_cell_volume_input")
    st.session_state.fuel_cell_volume = fuel_cell_volume

with st.sidebar.expander(t("shell_params_expander"), expanded=True):
    # 外壳形状选择
    container_shape = st.selectbox(
        t("container_shape"),
        [t("cylinder"), t("cuboid"), t("custom")],
        help=t("help_container_shape"),
        key="container_shape_input"
    )
    st.session_state.container_shape = container_shape

    if container_shape == t("cylinder"):
        cylinder_input_mode = st.radio(t("cylinder_input_mode"), [t("by_radius"), t("by_height"), t("minimum_surface")], help=t("help_cylinder_input"), key="cylinder_input_mode_input")
        st.session_state.cylinder_input_mode = cylinder_input_mode
        if cylinder_input_mode == t("by_radius"):
            container_radius_mm = st.number_input(f"{t('container_radius')} ({t('mm_unit')})", min_value=1.0, value=st.session_state.container_radius * 1000, step=1.0, help=t("help_container_radius"), key="container_radius_mm_input")
            container_radius = container_radius_mm / 1000
            container_height = None
            st.session_state.container_radius = container_radius
        elif cylinder_input_mode == t("by_height"):
            container_height_mm = st.number_input(f"{t('container_height')} ({t('mm_unit')})", min_value=1.0, value=st.session_state.container_height_input * 1000, step=1.0, help=t("help_container_height"), key="container_height_mm_input")
            container_height = container_height_mm / 1000
            container_radius = None
            st.session_state.container_height_input = container_height
        else:
            container_radius = None
            container_height = None
            st.info(f"✅ {t('minimum_surface')}: {t('minimum_surface_info1')}")
        container_length = None
        container_width = None
        container_count = st.number_input(f"{t('container_count')} ({t('container_count_unit')})", min_value=1, value=st.session_state.container_count, step=1, help=t("help_container_count"), key="container_count_input")
        st.session_state.container_count = container_count
        filling_ratio = st.number_input(f"{t('filling_ratio')} (%)", min_value=0.0, max_value=100.0, value=st.session_state.filling_ratio, step=1.0, help=t("help_filling_ratio"), key="filling_ratio_input")
        st.session_state.filling_ratio = filling_ratio
        container_thickness_mm = st.number_input(f"{t('container_thickness')} ({t('mm_unit')})", min_value=0.0, value=st.session_state.container_thickness * 1000, step=0.1, help=t("help_container_thickness"), key="container_thickness_mm_input")
        container_thickness = container_thickness_mm / 1000
        st.session_state.container_thickness = container_thickness

    elif container_shape == t("cuboid"):
        container_length_mm = st.number_input(f"{t('container_length')} ({t('mm_unit')})", min_value=1.0, value=st.session_state.container_length * 1000, step=1.0, help=t("help_container_length"), key="container_length_mm_input")
        container_width_mm = st.number_input(f"{t('container_width')} ({t('mm_unit')})", min_value=1.0, value=st.session_state.container_width * 1000, step=1.0, help=t("help_container_width"), key="container_width_mm_input")
        container_length = container_length_mm / 1000
        container_width = container_width_mm / 1000
        container_radius = None
        container_height = None
        st.session_state.container_length = container_length
        st.session_state.container_width = container_width
        container_count = st.number_input(f"{t('container_count')} ({t('container_count_unit')})", min_value=1, value=st.session_state.container_count, step=1, help=t("help_container_count"), key="container_count_input")
        st.session_state.container_count = container_count
        filling_ratio = st.number_input(f"{t('filling_ratio')} (%)", min_value=0.0, max_value=100.0, value=st.session_state.filling_ratio, step=1.0, help=t("help_filling_ratio"), key="filling_ratio_input")
        st.session_state.filling_ratio = filling_ratio
        container_thickness_mm = st.number_input(f"{t('container_thickness')} ({t('mm_unit')})", min_value=0.0, value=st.session_state.container_thickness * 1000, step=0.1, help=t("help_container_thickness"), key="container_thickness_mm_input")
        container_thickness = container_thickness_mm / 1000
        st.session_state.container_thickness = container_thickness

    else:  # 自定义
        st.info(t("custom_shape_note"))
        # 材料需求定义方式
        demand_mode = st.radio(
            t("material_demand_mode"),
            [t("mode_power"), t("mode_volume")],
            key="material_demand_mode_radio"
        )
        st.session_state.material_demand_mode = demand_mode

        # 壳体体积（固体材料体积）—— 输入以升为单位，内部存储为m³
        custom_solid_volume_L = st.number_input(
            f"{t('custom_shell_mass')} ({t('custom_shell_mass_unit')})",
            min_value=0.0,
            value=st.session_state.custom_shell_volume * 1000,
            step=0.001,
            format="%.3f",
            key="custom_solid_volume_input_L"
        )
        custom_solid_volume = custom_solid_volume_L / 1000.0
        st.session_state.custom_shell_volume = custom_solid_volume

        if demand_mode == t("mode_volume"):
            internal_vol_L = st.number_input(
                f"{t('custom_internal_volume')} ({t('custom_internal_volume_unit')})",
                min_value=0.0,
                value=st.session_state.custom_internal_volume * 1000,
                step=0.001,
                format="%.3f",
                help=t("custom_internal_note"),
                key="custom_internal_volume_input_L"
            )
            st.session_state.custom_internal_volume = internal_vol_L / 1000.0
            fill_ratio = st.number_input(
                f"{t('filling_ratio')} (%)",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.filling_ratio,
                step=1.0,
                key="custom_filling_ratio_input"
            )
            st.session_state.filling_ratio = fill_ratio
        else:
            fill_ratio = st.number_input(
                f"{t('filling_ratio')} (%)",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.filling_ratio,
                step=1.0,
                key="custom_filling_ratio_power"
            )
            st.session_state.filling_ratio = fill_ratio

        st.session_state.container_count = 1
        st.session_state.container_thickness = 0.0

    # 外壳材料
    st.subheader(t("shell_material"))
    shell_material_option = st.radio(t("shell_material"), [t("material_option_preset"), t("material_option_custom")], help=t("help_shell_material"), key="shell_material_option_input")
    st.session_state.shell_material_option = shell_material_option
    if shell_material_option == t("material_option_preset"):
        selected_shell_material = st.selectbox(t("select_preset_material"), list(PRESET_SHELL_MATERIALS.keys()), format_func=lambda x: f"{PRESET_SHELL_MATERIALS[x]['display_name'][st.session_state.language]} - {PRESET_SHELL_MATERIALS[x]['description'][st.session_state.language]}", help=t("help_preset_shell_material"), key="selected_shell_material_input")
        st.session_state.selected_shell_material = selected_shell_material
        shell_material_data = PRESET_SHELL_MATERIALS[selected_shell_material]
        shell_density = shell_material_data["density"]
        st.session_state.shell_density = shell_density
        st.markdown(f"**{t('shell_material_params')}**")
        st.text(f"{t('material')}: {PRESET_SHELL_MATERIALS[selected_shell_material]['display_name'][st.session_state.language]}")
        st.text(f"{t('shell_density')}: {shell_density} {t('material_density_unit')}")
        st.text(f"{t('description')}: {shell_material_data['description'][st.session_state.language]}")
    else:
        shell_density = st.number_input(f"{t('shell_density')} ({t('material_density_unit')})", min_value=0, value=st.session_state.shell_density, step=10, help=t("help_shell_density"), key="custom_shell_density_input")
        st.session_state.shell_density = shell_density

with st.sidebar.expander(t("battery_params_expander"), expanded=True):
    li_battery_mass_density = st.number_input(f"{t('li_battery_mass_density')} ({t('kwh_kg')})", min_value=0.0, value=st.session_state.li_battery_mass_density, step=0.01, help=t("help_li_battery_mass"), key="li_battery_mass_density_input")
    st.session_state.li_battery_mass_density = li_battery_mass_density
    li_battery_volume_density = st.number_input(f"{t('li_battery_volume_density')} ({t('kwh_m3')})", min_value=0, value=st.session_state.li_battery_volume_density, step=10, help=t("help_li_battery_volume"), key="li_battery_volume_density_input")
    st.session_state.li_battery_volume_density = li_battery_volume_density

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Current Settings" if st.session_state.language == "en" else "### 📊 当前设置")
if st.session_state.material_option == t("material_option_preset"):
    st.sidebar.markdown(f"**{t('current_material')}**: {st.session_state.selected_material}")
    st.sidebar.markdown(f"*{PRESET_MATERIALS[st.session_state.selected_material]['description'][st.session_state.language]}*")
else:
    st.sidebar.markdown(f"**{t('current_material')}**: {t('material_option_custom')}")
if st.session_state.shell_material_option == t("material_option_preset"):
    st.sidebar.markdown(f"**{t('current_shell_material')}**: {PRESET_SHELL_MATERIALS[st.session_state.selected_shell_material]['display_name'][st.session_state.language]}")
else:
    st.sidebar.markdown(f"**{t('current_shell_material')}**: {t('material_option_custom')}")
st.sidebar.markdown(f"**{t('current_fuel_cell_efficiency')}**: {st.session_state.fuel_cell_efficiency:.1f}%")
st.sidebar.markdown(f"**{t('current_container_shape')}**: {st.session_state.container_shape}")
if st.session_state.container_shape != t("custom"):
    st.sidebar.markdown(f"**{t('current_container_count')}**: {st.session_state.container_count}")
if st.session_state.container_shape == t("cylinder"):
    st.sidebar.markdown(f"**{t('cylinder_input_mode')}**: {st.session_state.cylinder_input_mode}")
if st.session_state.container_shape != t("custom"):
    st.sidebar.markdown(f"**{t('filling_ratio')}**: {st.session_state.filling_ratio:.1f}%")
if st.session_state.container_shape != t("custom") and st.session_state.container_thickness == 0:
    st.sidebar.markdown(f"**{t('shell_status')}**: {t('no_shell')}")
if st.session_state.container_shape == t("custom"):
    st.sidebar.markdown(f"**壳体体积**: {st.session_state.custom_shell_volume * 1000:.3f} L")
    if st.session_state.material_demand_mode == t("mode_volume"):
        st.sidebar.markdown(f"**内部容积**: {st.session_state.custom_internal_volume * 1000:.3f} L")
    st.sidebar.markdown(f"**{t('filling_ratio')}**: {st.session_state.filling_ratio:.1f}%")

# 主标签页
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    t("results_tab"),
    t("comparison_tab"),
    t("explanation_tab"),
    t("materials_tab"),
    t("principle_tab"),
    t("batch_export")
])

# ==================== 从session_state获取所有参数 ====================
if st.session_state.material_option == t("material_option_preset"):
    material_data = PRESET_MATERIALS[st.session_state.selected_material]
    dehydrogenation_enthalpy = material_data["dehydrogenation_enthalpy"]
    material_density = material_data["material_density"]
    hydrogen_mass_fraction = material_data["hydrogen_mass_fraction"]
else:
    dehydrogenation_enthalpy = st.session_state.dehydrogenation_enthalpy
    material_density = st.session_state.material_density
    hydrogen_mass_fraction = st.session_state.hydrogen_mass_fraction

fuel_cell_efficiency = st.session_state.fuel_cell_efficiency
output_power = st.session_state.output_power
endurance_time = st.session_state.endurance_time
fuel_cell_mass = st.session_state.fuel_cell_mass
fuel_cell_volume = st.session_state.fuel_cell_volume
container_shape = st.session_state.container_shape
cylinder_input_mode = st.session_state.cylinder_input_mode
container_radius = st.session_state.container_radius if hasattr(st.session_state, 'container_radius') else None
container_height_input = st.session_state.container_height_input if hasattr(st.session_state, 'container_height_input') else None
container_length = st.session_state.container_length if hasattr(st.session_state, 'container_length') else None
container_width = st.session_state.container_width if hasattr(st.session_state, 'container_width') else None
container_count = st.session_state.container_count
filling_ratio = st.session_state.filling_ratio
container_thickness = st.session_state.container_thickness
shell_density = st.session_state.shell_density
li_battery_mass_density = st.session_state.li_battery_mass_density
li_battery_volume_density = st.session_state.li_battery_volume_density

# 自定义参数（内部存储为m³）
custom_shell_solid_volume = st.session_state.custom_shell_volume
custom_internal_volume = st.session_state.custom_internal_volume if hasattr(st.session_state, 'custom_internal_volume') else 0.0
material_demand_mode = st.session_state.material_demand_mode if hasattr(st.session_state, 'material_demand_mode') else t("mode_power")

# ==================== 计算核心 ====================
# 基础材料能量密度（不变）
moles_per_kg_h2 = 500
dehydrogenation_energy_consumption = (dehydrogenation_enthalpy * moles_per_kg_h2) / 3600
fuel_cell_power_generation = (H2_ENERGY_DENSITY - dehydrogenation_energy_consumption) * (fuel_cell_efficiency / 100)
net_power_generation = fuel_cell_power_generation
material_mass_energy_density = net_power_generation / (1 / hydrogen_mass_fraction)
material_volume_energy_density = material_mass_energy_density * material_density

# 判断是否由外壳容积定义材料量
use_volume_mode = (container_shape == t("custom") and material_demand_mode == t("mode_volume"))

if use_volume_mode:
    material_volume_required = custom_internal_volume * (filling_ratio / 100.0)
    material_mass_required = material_volume_required * material_density
    total_energy_required = material_mass_required * material_mass_energy_density
    output_power_effective = 0.0
    endurance_time_effective = 0.0
else:
    total_energy_required = output_power * endurance_time
    material_mass_required = total_energy_required / material_mass_energy_density
    material_volume_required = total_energy_required / material_volume_energy_density
    output_power_effective = output_power
    endurance_time_effective = endurance_time

# 无外壳系统
system_total_mass_no_shell = material_mass_required + fuel_cell_mass
system_total_volume_no_shell = material_volume_required + (fuel_cell_volume / 1000)
system_mass_energy_density_no_shell = total_energy_required / system_total_mass_no_shell
system_volume_energy_density_no_shell = total_energy_required / system_total_volume_no_shell

# ==================== 外壳计算 ====================
if container_shape == t("custom"):
    solid_volume = custom_shell_solid_volume
    if use_volume_mode:
        internal_vol = custom_internal_volume
        total_shell_volume = internal_vol + solid_volume
        total_shell_mass = solid_volume * shell_density
        single_shell_volume = total_shell_volume
        single_shell_mass = total_shell_mass
        calculated_container_height = None
        calculated_container_radius = None
    else:
        internal_vol = material_volume_required / (filling_ratio / 100.0) if filling_ratio > 0 else 0
        total_shell_volume = internal_vol + solid_volume
        total_shell_mass = solid_volume * shell_density
        single_shell_volume = total_shell_volume
        single_shell_mass = total_shell_mass
        calculated_container_height = None
        calculated_container_radius = None
else:
    if container_thickness == 0:
        single_shell_volume = 0
        single_shell_mass = 0
        total_shell_volume = 0
        total_shell_mass = 0
        calculated_container_height = None
        calculated_container_radius = None
    else:
        material_volume_per_container = material_volume_required / container_count
        internal_volume_per_container = material_volume_per_container / (filling_ratio / 100)
        if container_shape == t("cylinder"):
            if cylinder_input_mode == t("by_radius"):
                base_area = math.pi * container_radius ** 2
                calculated_container_height = internal_volume_per_container / base_area
                outer_volume = base_area * calculated_container_height
                inner_radius = container_radius - container_thickness
                inner_base_area = math.pi * inner_radius ** 2 if inner_radius > 0 else 0
                inner_volume = inner_base_area * (calculated_container_height - 2 * container_thickness) if inner_radius > 0 and calculated_container_height > 2 * container_thickness else 0
                single_shell_volume = outer_volume - inner_volume
            elif cylinder_input_mode == t("by_height"):
                container_height_m = container_height_input
                calculated_container_radius = math.sqrt(internal_volume_per_container / (math.pi * container_height_m))
                base_area = math.pi * calculated_container_radius ** 2
                outer_volume = base_area * container_height_m
                inner_radius = calculated_container_radius - container_thickness
                inner_base_area = math.pi * inner_radius ** 2 if inner_radius > 0 else 0
                inner_volume = inner_base_area * (container_height_m - 2 * container_thickness) if inner_radius > 0 and container_height_m > 2 * container_thickness else 0
                single_shell_volume = outer_volume - inner_volume
            else:
                calculated_container_radius = (internal_volume_per_container / (2 * math.pi)) ** (1/3)
                calculated_container_height = 2 * calculated_container_radius
                base_area = math.pi * calculated_container_radius ** 2
                outer_volume = base_area * calculated_container_height
                inner_radius = calculated_container_radius - container_thickness
                inner_base_area = math.pi * inner_radius ** 2 if inner_radius > 0 else 0
                inner_volume = inner_base_area * (calculated_container_height - 2 * container_thickness) if inner_radius > 0 and calculated_container_height > 2 * container_thickness else 0
                single_shell_volume = outer_volume - inner_volume
        else:
            base_area = container_length * container_width
            calculated_container_height = internal_volume_per_container / base_area
            outer_volume = container_length * container_width * calculated_container_height
            inner_length = container_length - 2 * container_thickness
            inner_width = container_width - 2 * container_thickness
            inner_height = calculated_container_height - 2 * container_thickness
            inner_volume = inner_length * inner_width * inner_height if inner_length > 0 and inner_width > 0 and inner_height > 0 else 0
            single_shell_volume = outer_volume - inner_volume
        single_shell_mass = single_shell_volume * shell_density
        total_shell_volume = single_shell_volume * container_count
        total_shell_mass = single_shell_mass * container_count

system_total_mass_with_shell = material_mass_required + fuel_cell_mass + total_shell_mass
system_total_volume_with_shell = material_volume_required + (fuel_cell_volume / 1000) + total_shell_volume
system_mass_energy_density_with_shell = total_energy_required / system_total_mass_with_shell
system_volume_energy_density_with_shell = total_energy_required / system_total_volume_with_shell

# ==================== 标签页1：计算结果 ====================
with tab1:
    st.markdown(f'<h2 class="section-header">{t("basic_calculation")}</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔋 Basic Energy Parameters" if st.session_state.language == "en" else "🔋 基础能量参数")
        st.metric(t("h2_energy_density"), f"{H2_ENERGY_DENSITY} {t('kwh_kg')}")
        st.metric(t("dehydrogenation_energy"), f"{dehydrogenation_energy_consumption:.2f} kWh/kgH₂")
        st.metric(t("net_power"), f"{net_power_generation:.2f} kWh/kgH₂")
    with col2:
        st.subheader("📊 Material Energy Density" if st.session_state.language == "en" else "📊 材料能量密度")
        st.metric(f"{t('mass_energy_density')}", f"{material_mass_energy_density:.3f} {t('kwh_kg')}")
        st.metric(f"{t('volume_energy_density')}", f"{material_volume_energy_density:.1f} {t('kwh_m3')}")

    st.markdown(f'<h2 class="section-header">{t("system_calculation_no_shell")}</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"📦 {t('system_requirements')} ({t('no_shell')})")
        if use_volume_mode:
            st.metric("总储能能量", f"{total_energy_required:.1f} kWh")
            st.metric("材料质量", f"{material_mass_required:.1f} kg")
            st.metric("材料体积", f"{material_volume_required * 1000:.3f} L")
        else:
            st.metric(t("total_energy_required"), f"{total_energy_required:.1f} kWh")
            st.metric(t("material_mass_required"), f"{material_mass_required:.1f} kg")
            st.metric(t("material_volume_required"), f"{material_volume_required * 1000:.3f} L")
    with col2:
        st.subheader(f"⚖️ {t('system_total')} ({t('no_shell')})")
        st.metric(t("system_total_mass"), f"{system_total_mass_no_shell:.1f} kg")
        st.metric(t("system_total_volume"), f"{system_total_volume_no_shell * 1000:.3f} L")
        st.metric(t("system_mass_energy_density"), f"{system_mass_energy_density_no_shell:.3f} {t('kwh_kg')}")
        st.metric(t("system_volume_energy_density"), f"{system_volume_energy_density_no_shell:.1f} {t('kwh_m3')}")

    st.markdown(f'<h2 class="section-header">{t("system_calculation_with_shell")}</h2>', unsafe_allow_html=True)

    if container_shape == t("custom"):
        st.subheader("🛠️ " + t("custom_shape_note"))
        col1, col2 = st.columns(2)
        with col1:
            st.metric("壳体体积 (固体材料)", f"{custom_shell_solid_volume * 1000:.3f} L")
            if use_volume_mode:
                st.metric("内部容积", f"{custom_internal_volume * 1000:.3f} L")
            st.metric("填充率", f"{filling_ratio:.1f}%")
            st.metric("外壳总质量", f"{total_shell_mass:.1f} kg")
            st.metric("外壳总体积", f"{total_shell_volume * 1000:.3f} L")
        with col2:
            if use_volume_mode:
                st.metric("总储能能量", f"{total_energy_required:.1f} kWh")
            else:
                st.metric(t("total_energy_required"), f"{total_energy_required:.1f} kWh")
            st.metric(t("system_total_mass"), f"{system_total_mass_with_shell:.1f} kg")
            st.metric(t("system_total_volume"), f"{system_total_volume_with_shell * 1000:.3f} L")
            st.metric(t("system_mass_energy_density"), f"{system_mass_energy_density_with_shell:.3f} {t('kwh_kg')}")
            st.metric(t("system_volume_energy_density"), f"{system_volume_energy_density_with_shell:.1f} {t('kwh_m3')}")
    else:
        if container_thickness == 0:
            st.subheader(t("shell_status"))
            st.info(f"🔓 {t('container_thickness')} 0，{t('no_shell')}")
        else:
            st.info(f"📊 {t('container_count')}: {container_count} {t('container_count_unit')}")
            if container_shape == t("cylinder"):
                if cylinder_input_mode == t("by_radius"):
                    st.subheader(f"📏 {t('single_shell_dimensions')} ({t('cylinder')}-{t('by_radius')})")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1: st.metric(t("container_radius"), f"{container_radius * 1000:.1f} {t('mm_unit')}")
                    with col2: st.metric(t("container_height"), f"{calculated_container_height * 1000:.1f} {t('mm_unit')}")
                    with col3: st.metric(t("container_thickness"), f"{container_thickness * 1000:.1f} {t('mm_unit')}")
                    with col4: st.metric(t("filling_ratio"), f"{filling_ratio:.1f}%")
                    with col5: st.metric(t("material_per_container"), f"{material_volume_per_container * 1000:.3f} L")
                elif cylinder_input_mode == t("by_height"):
                    st.subheader(f"📏 {t('single_shell_dimensions')} ({t('cylinder')}-{t('by_height')})")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1: st.metric(t("container_radius"), f"{calculated_container_radius * 1000:.1f} {t('mm_unit')}")
                    with col2: st.metric(t("container_height"), f"{container_height_input * 1000:.1f} {t('mm_unit')}")
                    with col3: st.metric(t("container_thickness"), f"{container_thickness * 1000:.1f} {t('mm_unit')}")
                    with col4: st.metric(t("filling_ratio"), f"{filling_ratio:.1f}%")
                    with col5: st.metric(t("material_per_container"), f"{material_volume_per_container * 1000:.3f} L")
                else:
                    st.subheader(f"📏 {t('single_shell_dimensions')} ({t('cylinder')}-{t('minimum_surface')})")
                    col1, col2, col3, col4, col5, col6 = st.columns(6)
                    with col1: st.metric(t("container_radius"), f"{calculated_container_radius * 1000:.1f} {t('mm_unit')}")
                    with col2: st.metric(t("container_height"), f"{calculated_container_height * 1000:.1f} {t('mm_unit')}")
                    with col3: st.metric(t("container_thickness"), f"{container_thickness * 1000:.1f} {t('mm_unit')}")
                    with col4: st.metric(t("filling_ratio"), f"{filling_ratio:.1f}%")
                    with col5: st.metric(t("material_per_container"), f"{material_volume_per_container * 1000:.3f} L")
                    with col6: st.metric(t("container_count"), f"{container_count}")
                    st.info(f"✅ {t('minimum_surface')}: {t('minimum_surface_info2')}")
            else:
                st.subheader(f"📏 {t('single_shell_dimensions')} ({t('cuboid')})")
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1: st.metric(t("container_length"), f"{container_length * 1000:.1f} {t('mm_unit')}")
                with col2: st.metric(t("container_width"), f"{container_width * 1000:.1f} {t('mm_unit')}")
                with col3: st.metric(t("container_height"), f"{calculated_container_height * 1000:.1f} {t('mm_unit')}")
                with col4: st.metric(t("container_thickness"), f"{container_thickness * 1000:.1f} {t('mm_unit')}")
                with col5: st.metric(t("filling_ratio"), f"{filling_ratio:.1f}%")
                with col6: st.metric(t("material_per_container"), f"{material_volume_per_container * 1000:.3f} L")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"🛡️ {t('shell_parameters')}")
            st.markdown(f"**{t('single_shell_parameters')}:**")
            st.metric(t("single_shell_volume"), f"{single_shell_volume * 1000:.3f} L")
            st.metric(t("single_shell_mass"), f"{single_shell_mass:.1f} kg")
            st.markdown(f"**{t('total_shell_parameters')} ({container_count} {t('container_count_unit')}):**")
            st.metric(t("total_shell_volume"), f"{total_shell_volume * 1000:.3f} L")
            st.metric(t("total_shell_mass"), f"{total_shell_mass:.1f} kg")
            if st.session_state.shell_material_option == t("material_option_preset"):
                shell_material_display_name = PRESET_SHELL_MATERIALS[st.session_state.selected_shell_material]['display_name'][st.session_state.language]
                st.metric(t("shell_material"), f"{shell_material_display_name}")
            else:
                st.metric(t("shell_material"), t("material_option_custom"))
            st.metric(t("shell_density"), f"{shell_density} {t('material_density_unit')}")
        with col2:
            st.subheader(f"⚖️ {t('system_total')} ({t('with_shell')})")
            st.metric(t("system_total_mass"), f"{system_total_mass_with_shell:.1f} kg")
            st.metric(t("system_total_volume"), f"{system_total_volume_with_shell * 1000:.3f} L")
            st.metric(t("system_mass_energy_density"), f"{system_mass_energy_density_with_shell:.3f} {t('kwh_kg')}")
            st.metric(t("system_volume_energy_density"), f"{system_volume_energy_density_with_shell:.1f} {t('kwh_m3')}")

    # 桑基图（不变）
    st.markdown(f'<h2 class="section-header">{t("energy_density_dilution_sankey")}</h2>', unsafe_allow_html=True)
    st.markdown(f"**{t('energy_density_dilution_description')}**")
    h2_mass_in_1kg_material = 1 * hydrogen_mass_fraction
    total_hydrogen_energy = h2_mass_in_1kg_material * H2_ENERGY_DENSITY
    dehydrogenation_energy_mass = h2_mass_in_1kg_material * dehydrogenation_energy_consumption
    remaining_chemical_energy = total_hydrogen_energy - dehydrogenation_energy_mass
    fuel_cell_loss = remaining_chemical_energy * (1 - fuel_cell_efficiency / 100)
    net_electrical_output = material_mass_energy_density
    stack_dilution_mass = material_mass_energy_density - system_mass_energy_density_no_shell
    shell_dilution_mass = system_mass_energy_density_no_shell - system_mass_energy_density_with_shell
    labels = [t("hydrogen_chemical_energy"), t("dehydrogenation_energy_loss"), t("remaining_chemical_energy"),
              t("fuel_cell_efficiency_loss"), t("material_energy_density"), t("stack_dilution_effect"),
              t("system_energy_density_no_shell"), t("shell_dilution_effect"), t("final_system_energy_density")]
    source = [0, 0, 2, 2, 4, 4, 6, 6]
    target = [1, 2, 3, 4, 5, 6, 7, 8]
    value = [dehydrogenation_energy_mass, remaining_chemical_energy, fuel_cell_loss, net_electrical_output,
             stack_dilution_mass, system_mass_energy_density_no_shell, shell_dilution_mass,
             system_mass_energy_density_with_shell]
    node_colors = ['rgba(31,119,180,0.8)', 'rgba(255,127,14,0.8)', 'rgba(44,160,44,0.8)', 'rgba(214,39,40,0.8)',
                   'rgba(148,103,189,0.8)', 'rgba(140,86,75,0.8)', 'rgba(227,119,194,0.8)', 'rgba(127,127,127,0.8)',
                   'rgba(188,189,34,0.8)']
    link_colors = ['rgba(255,127,14,0.4)', 'rgba(44,160,44,0.4)', 'rgba(214,39,40,0.4)', 'rgba(148,103,189,0.4)',
                   'rgba(140,86,75,0.4)', 'rgba(227,119,194,0.4)', 'rgba(127,127,127,0.4)', 'rgba(188,189,34,0.4)']
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels, color=node_colors),
        link=dict(source=source, target=target, value=value, color=link_colors)
    )])
    fig_sankey.update_layout(
        title=dict(text=f"{t('energy_density_flow')}", x=0.5, xanchor='center', font=dict(size=16, family="Arial", color='black')),
        font=dict(size=12, family="Arial"), height=600, margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='white', paper_bgcolor='white'
    )
    st.plotly_chart(fig_sankey, use_container_width=True)

    with st.expander(f"📖 {t('sankey_diagram_explanation')}"):
        st.markdown(f"**{t('sankey_explanation_text')}**")
        mass_retention_ratio = system_mass_energy_density_with_shell / material_mass_energy_density * 100
        volume_retention_ratio = system_volume_energy_density_with_shell / material_volume_energy_density * 100
        st.markdown(f"**{t('key_observations')}:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{t('mass_energy_density')}:**")
            st.markdown(f"- {t('material_energy_density')}: {material_mass_energy_density:.3f} {t('kwh_kg')}")
            st.markdown(f"- {t('dehydrogenation_impact')}: -{dehydrogenation_energy_mass / total_hydrogen_energy * 100:.1f}%")
            st.markdown(f"- {t('fuel_cell_impact')}: -{fuel_cell_loss / total_hydrogen_energy * 100:.1f}%")
            st.markdown(f"- {t('stack_mass_impact')}: -{stack_dilution_mass / material_mass_energy_density * 100:.1f}%")
            st.markdown(f"- {t('shell_mass_impact')}: -{shell_dilution_mass / material_mass_energy_density * 100:.1f}%")
            st.markdown(f"- {t('final_system_energy_density')}: {system_mass_energy_density_with_shell:.3f} {t('kwh_kg')}")
            st.markdown(f"- {t('total_dilution')}: {100 - mass_retention_ratio:.1f}%")
            st.markdown(f"- **{t('dilution_ratio')}**: {mass_retention_ratio:.1f}%")
        with col2:
            st.markdown(f"**{t('volume_energy_density')}:**")
            st.markdown(f"- {t('material_energy_density')}: {material_volume_energy_density:.1f} {t('kwh_m3')}")
            st.markdown(f"- {t('dehydrogenation_impact')}: -{dehydrogenation_energy_mass / total_hydrogen_energy * 100:.1f}%")
            st.markdown(f"- {t('fuel_cell_impact')}: -{fuel_cell_loss / total_hydrogen_energy * 100:.1f}%")
            volume_stack_dilution = material_volume_energy_density - system_volume_energy_density_no_shell
            volume_shell_dilution = system_volume_energy_density_no_shell - system_volume_energy_density_with_shell
            st.markdown(f"- {t('stack_mass_impact')}: -{volume_stack_dilution / material_volume_energy_density * 100:.1f}%")
            st.markdown(f"- {t('shell_mass_impact')}: -{volume_shell_dilution / material_volume_energy_density * 100:.1f}%")
            st.markdown(f"- {t('final_system_energy_density')}: {system_volume_energy_density_with_shell:.1f} {t('kwh_m3')}")
            st.markdown(f"- {t('total_dilution')}: {100 - volume_retention_ratio:.1f}%")
            st.markdown(f"- **{t('dilution_ratio')}**: {volume_retention_ratio:.1f}%")
        st.markdown(f"**{t('both_dilution_processes')}**")
        st.markdown("---")
        st.markdown(f"**{t('observation_1')}**: {dehydrogenation_energy_mass / total_hydrogen_energy * 100:.1f}%")
        st.markdown(f"**{t('observation_2')}**: {fuel_cell_loss / remaining_chemical_energy * 100:.1f}%")
        st.markdown(f"**{t('observation_3')}**: {stack_dilution_mass / material_mass_energy_density * 100:.1f}%")
        st.markdown(f"**{t('observation_4')}**: {shell_dilution_mass / material_mass_energy_density * 100:.1f}%")
        st.markdown(f"**{t('observation_5')}**: {mass_retention_ratio:.1f}% ({t('mass_energy_density')}) / {volume_retention_ratio:.1f}% ({t('volume_energy_density')})")

    st.success(t("calculation_complete"))

# ==================== 标签页2：性能对比 ====================
with tab2:
    if use_volume_mode:
        st.warning("当前模式为‘按外壳容积’，续航对比图表不适用。")
        st.info("请切换到‘按功率续航’模式查看系统能量密度随续航时间的变化。")
    else:
        st.markdown(f'<h2 class="section-header">{t("endurance_comparison")}</h2>', unsafe_allow_html=True)
        endurance_times = [1,2,3,4,5,6,7,8,9,10]
        system_mass_densities_no_shell = []
        system_volume_densities_no_shell = []
        system_mass_densities_with_shell = []
        system_volume_densities_with_shell = []
        for time in endurance_times:
            total_energy = output_power * time
            material_mass = total_energy / material_mass_energy_density
            material_volume = total_energy / material_volume_energy_density
            system_mass_no_shell = material_mass + fuel_cell_mass
            system_volume_no_shell = material_volume + (fuel_cell_volume / 1000)
            system_mass_densities_no_shell.append(total_energy / system_mass_no_shell)
            system_volume_densities_no_shell.append(total_energy / system_volume_no_shell)
            # 计算带外壳
            if container_shape == t("custom"):
                internal_vol = material_volume / (filling_ratio / 100.0) if filling_ratio > 0 else 0
                shell_vol = internal_vol + custom_shell_solid_volume
                shell_mass = custom_shell_solid_volume * shell_density
                system_mass_with_shell = material_mass + fuel_cell_mass + shell_mass
                system_volume_with_shell = material_volume + (fuel_cell_volume / 1000) + shell_vol
                system_mass_densities_with_shell.append(total_energy / system_mass_with_shell)
                system_volume_densities_with_shell.append(total_energy / system_volume_with_shell)
            else:
                if container_thickness == 0:
                    system_mass_densities_with_shell.append(total_energy / system_mass_no_shell)
                    system_volume_densities_with_shell.append(total_energy / system_volume_no_shell)
                else:
                    material_volume_per_container_time = material_volume / container_count
                    internal_volume_per_container = material_volume_per_container_time / (filling_ratio / 100)
                    if container_shape == t("cylinder"):
                        if cylinder_input_mode == t("by_radius"):
                            base_area = math.pi * container_radius ** 2
                            container_height_calc = internal_volume_per_container / base_area
                            outer_vol = base_area * container_height_calc
                            inner_rad = container_radius - container_thickness
                            inner_base = math.pi * inner_rad ** 2 if inner_rad > 0 else 0
                            inner_vol = inner_base * (container_height_calc - 2 * container_thickness) if inner_rad > 0 and container_height_calc > 2 * container_thickness else 0
                            single_shell_vol = outer_vol - inner_vol
                        elif cylinder_input_mode == t("by_height"):
                            height_m = container_height_input
                            rad = math.sqrt(internal_volume_per_container / (math.pi * height_m))
                            base_area = math.pi * rad ** 2
                            outer_vol = base_area * height_m
                            inner_rad = rad - container_thickness
                            inner_base = math.pi * inner_rad ** 2 if inner_rad > 0 else 0
                            inner_vol = inner_base * (height_m - 2 * container_thickness) if inner_rad > 0 and height_m > 2 * container_thickness else 0
                            single_shell_vol = outer_vol - inner_vol
                        else:
                            rad = (internal_volume_per_container / (2 * math.pi)) ** (1/3)
                            height_calc = 2 * rad
                            base_area = math.pi * rad ** 2
                            outer_vol = base_area * height_calc
                            inner_rad = rad - container_thickness
                            inner_base = math.pi * inner_rad ** 2 if inner_rad > 0 else 0
                            inner_vol = inner_base * (height_calc - 2 * container_thickness) if inner_rad > 0 and height_calc > 2 * container_thickness else 0
                            single_shell_vol = outer_vol - inner_vol
                    else:
                        base_area = container_length * container_width
                        container_height_calc = internal_volume_per_container / base_area
                        outer_vol = container_length * container_width * container_height_calc
                        inner_len = container_length - 2 * container_thickness
                        inner_wid = container_width - 2 * container_thickness
                        inner_hei = container_height_calc - 2 * container_thickness
                        inner_vol = inner_len * inner_wid * inner_hei if inner_len>0 and inner_wid>0 and inner_hei>0 else 0
                        single_shell_vol = outer_vol - inner_vol
                    single_shell_mass_temp = single_shell_vol * shell_density
                    total_shell_mass_temp = single_shell_mass_temp * container_count
                    total_shell_volume_temp = single_shell_vol * container_count
                    system_mass_with_shell = material_mass + fuel_cell_mass + total_shell_mass_temp
                    system_volume_with_shell = material_volume + (fuel_cell_volume / 1000) + total_shell_volume_temp
                    system_mass_densities_with_shell.append(total_energy / system_mass_with_shell)
                    system_volume_densities_with_shell.append(total_energy / system_volume_with_shell)

        df = pd.DataFrame({
            f'{t("endurance_time_h")}': endurance_times,
            f'{t("system_mass_energy_density")}-{t("no_shell")} ({t("kwh_kg")})': [f"{x:.3f}" for x in system_mass_densities_no_shell],
            f'{t("system_volume_energy_density")}-{t("no_shell")} ({t("kwh_m3")})': [f"{x:.1f}" for x in system_volume_densities_no_shell],
            f'{t("system_mass_energy_density")}-{t("with_shell")} ({t("kwh_kg")})': [f"{x:.3f}" for x in system_mass_densities_with_shell],
            f'{t("system_volume_energy_density")}-{t("with_shell")} ({t("kwh_m3")})': [f"{x:.1f}" for x in system_volume_densities_with_shell]
        })
        st.dataframe(df, width='stretch')
        col1, col2 = st.columns(2)
        with col1:
            fig_mass = go.Figure()
            fig_mass.add_trace(go.Scatter(x=endurance_times, y=system_mass_densities_no_shell, mode='lines+markers', name=f'{t("system_mass_energy_density")}-{t("no_shell")}', line=dict(color='#1f77b4', width=3), marker=dict(size=8)))
            fig_mass.add_trace(go.Scatter(x=endurance_times, y=system_mass_densities_with_shell, mode='lines+markers', name=f'{t("system_mass_energy_density")}-{t("with_shell")}', line=dict(color='#ff7f0e', width=3, dash='dash'), marker=dict(size=8, symbol='square')))
            fig_mass.add_trace(go.Scatter(x=[min(endurance_times), max(endurance_times)], y=[material_mass_energy_density, material_mass_energy_density], mode='lines', name=f'{t("material")} {t("mass_energy_density")}', line=dict(color='#2ca02c', width=2, dash='dot')))
            fig_mass.add_trace(go.Scatter(x=[min(endurance_times), max(endurance_times)], y=[li_battery_mass_density, li_battery_mass_density], mode='lines', name=f'{t("li_battery_mass_density")}', line=dict(color='#d62728', width=2, dash='dashdot')))
            fig_mass.update_layout(title=dict(text=t("mass_energy_density_vs_time"), x=0.5), xaxis_title=t("endurance_time_h"), yaxis_title=t("mass_energy_density_unit"), legend=dict(x=0.98, y=0.12, bgcolor='rgba(255,255,255,0.9)'), plot_bgcolor='white', height=500)
            st.plotly_chart(fig_mass, use_container_width=True)
        with col2:
            fig_volume = go.Figure()
            fig_volume.add_trace(go.Scatter(x=endurance_times, y=system_volume_densities_no_shell, mode='lines+markers', name=f'{t("system_volume_energy_density")}-{t("no_shell")}', line=dict(color='#1f77b4', width=3), marker=dict(size=8)))
            fig_volume.add_trace(go.Scatter(x=endurance_times, y=system_volume_densities_with_shell, mode='lines+markers', name=f'{t("system_volume_energy_density")}-{t("with_shell")}', line=dict(color='#ff7f0e', width=3, dash='dash'), marker=dict(size=8, symbol='square')))
            fig_volume.add_trace(go.Scatter(x=[min(endurance_times), max(endurance_times)], y=[material_volume_energy_density, material_volume_energy_density], mode='lines', name=f'{t("material")} {t("volume_energy_density")}', line=dict(color='#2ca02c', width=2, dash='dot')))
            fig_volume.add_trace(go.Scatter(x=[min(endurance_times), max(endurance_times)], y=[li_battery_volume_density, li_battery_volume_density], mode='lines', name=f'{t("li_battery_volume_density")}', line=dict(color='#d62728', width=2, dash='dashdot')))
            fig_volume.update_layout(title=dict(text=t("volume_energy_density_vs_time"), x=0.5), xaxis_title=t("endurance_time_h"), yaxis_title=t("volume_energy_density_unit"), legend=dict(x=0.98, y=0.12, bgcolor='rgba(255,255,255,0.9)'), plot_bgcolor='white', height=500)
            st.plotly_chart(fig_volume, use_container_width=True)

        # 雷达图（不变）
        st.markdown("---")
        analysis_title_zh = "多维度材料性能对比分析"
        analysis_title_en = "Multi-dimensional Material Performance Comparison Analysis"
        analysis_title = analysis_title_zh if st.session_state.language == 'zh' else analysis_title_en
        st.markdown(f'<h2 class="section-header">{analysis_title}</h2>', unsafe_allow_html=True)
        subtab1, subtab2 = st.tabs(["📊 雷达图对比", "📦 系统组成分析"] if st.session_state.language=='zh' else ["📊 Radar Chart", "📦 System Composition"])
        with subtab1:
            st.markdown("### 材料性能雷达图对比" if st.session_state.language=='zh' else "### Material Performance Radar Chart Comparison")
            radar_categories_zh = ['质量能量密度 (kWh/kg)', '体积能量密度 (kWh/m³)', '储氢密度 (%)', '脱氢焓变 (kJ/mol)', '材料密度 (kg/m³)']
            radar_categories_en = ['Mass Energy Density (kWh/kg)', 'Volume Energy Density (kWh/m³)', 'Hydrogen Storage (%)', 'Dehydrogenation Enthalpy (kJ/mol)', 'Material Density (kg/m³)']
            radar_categories = radar_categories_zh if st.session_state.language == 'zh' else radar_categories_en
            materials_to_compare = list(PRESET_MATERIALS.keys())[:4]
            all_real_data = []
            for material in materials_to_compare:
                props = PRESET_MATERIALS[material]
                de_en = (props["dehydrogenation_enthalpy"] * 500) / 3600
                fc_power = H2_ENERGY_DENSITY * (fuel_cell_efficiency / 100)
                net_pow = fc_power - de_en
                mass_ed = net_pow / (1 / props["hydrogen_mass_fraction"])
                vol_ed = mass_ed * props["material_density"]
                real_data = [mass_ed, vol_ed, props["hydrogen_mass_fraction"]*100, props["dehydrogenation_enthalpy"], props["material_density"]]
                all_real_data.append(real_data)
            max_values = [max(dim)*1.1 for dim in zip(*all_real_data)] if all_real_data else [1,1,1,1,1]
            radar_data = []
            for i, material in enumerate(materials_to_compare):
                real_data = all_real_data[i]
                normalized = [real_data[j]/max_values[j] for j in range(5)]
                if st.session_state.language == 'zh':
                    hovertemplate = (f'<b>{material}</b><br>质量能量密度: {real_data[0]:.3f} kWh/kg<br>体积能量密度: {real_data[1]:.1f} kWh/m³<br>储氢密度: {real_data[2]:.2f}%<br>脱氢焓变: {real_data[3]:.1f} kJ/mol<br>材料密度: {real_data[4]:.0f} kg/m³<extra></extra>')
                else:
                    hovertemplate = (f'<b>{material}</b><br>Mass Energy Density: {real_data[0]:.3f} kWh/kg<br>Volume Energy Density: {real_data[1]:.1f} kWh/m³<br>Hydrogen Storage: {real_data[2]:.2f}%<br>Dehydrogenation Enthalpy: {real_data[3]:.1f} kJ/mol<br>Material Density: {real_data[4]:.0f} kg/m³<extra></extra>')
                radar_data.append(go.Scatterpolar(r=normalized+[normalized[0]], theta=radar_categories+[radar_categories[0]], fill='toself', name=material, hovertemplate=hovertemplate))
            fig_radar = go.Figure(data=radar_data)
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])), showlegend=True, title=dict(text="材料性能雷达图对比（归一化显示）" if st.session_state.language=='zh' else "Material Performance Radar Chart Comparison (Normalized Display)", x=0.5), height=500)
            st.plotly_chart(fig_radar, use_container_width=True)
            if st.session_state.language == 'zh':
                st.info("**雷达图说明**：使用归一化显示，每个维度的最大值为该维度所有材料中的最高值。悬停查看真实数值。")
            else:
                st.info("**Radar Chart Explanation**: Normalized display, maximum of each dimension is the highest value among materials. Hover for actual values.")

        with subtab2:
            st.markdown("### 系统质量与体积组成分析" if st.session_state.language=='zh' else "### System Mass and Volume Composition Analysis")
            if container_shape == t("custom"):
                total_mass = system_total_mass_with_shell
                total_volume = system_total_volume_with_shell
                mass_components = {'储氢材料': material_mass_required, '燃料电池': fuel_cell_mass, '外壳': total_shell_mass}
                volume_components = {'储氢材料': material_volume_required, '燃料电池': fuel_cell_volume/1000, '外壳': total_shell_volume}
            else:
                if container_thickness > 0:
                    total_mass = system_total_mass_with_shell
                    total_volume = system_total_volume_with_shell
                    mass_components = {'储氢材料': material_mass_required, '燃料电池': fuel_cell_mass, '外壳': total_shell_mass}
                    volume_components = {'储氢材料': material_volume_required, '燃料电池': fuel_cell_volume/1000, '外壳': total_shell_volume}
                else:
                    total_mass = system_total_mass_no_shell
                    total_volume = system_total_volume_no_shell
                    mass_components = {'储氢材料': material_mass_required, '燃料电池': fuel_cell_mass}
                    volume_components = {'储氢材料': material_volume_required, '燃料电池': fuel_cell_volume/1000}
            label_mapping = {'储氢材料': '储氢材料', '燃料电池': '燃料电池', '外壳': '外壳'} if st.session_state.language=='zh' else {'储氢材料': 'H₂ Storage Material', '燃料电池': 'Fuel Cell', '外壳': 'Shell'}
            col1, col2 = st.columns(2)
            with col1:
                fig_mass_pie = go.Figure(data=[go.Pie(labels=[label_mapping[k] for k in mass_components.keys()], values=list(mass_components.values()), hole=0.4, textinfo='percent+label')])
                fig_mass_pie.update_layout(title=dict(text=f"系统质量组成\n总计: {total_mass:.1f} kg" if st.session_state.language=='zh' else f"System Mass Composition\nTotal: {total_mass:.1f} kg", x=0.5), height=400)
                st.plotly_chart(fig_mass_pie, use_container_width=True)
            with col2:
                fig_volume_pie = go.Figure(data=[go.Pie(labels=[label_mapping[k] for k in volume_components.keys()], values=[v*1000 for v in volume_components.values()], hole=0.4, textinfo='percent+label')])
                fig_volume_pie.update_layout(title=dict(text=f"系统体积组成\n总计: {total_volume*1000:.3f} L" if st.session_state.language=='zh' else f"System Volume Composition\nTotal: {total_volume*1000:.3f} L", x=0.5), height=400)
                st.plotly_chart(fig_volume_pie, use_container_width=True)
            st.markdown("#### 组成详细数据" if st.session_state.language=='zh' else "#### Composition Details")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**质量组成 (kg)**" if st.session_state.language=='zh' else "**Mass Composition (kg)**")
                for comp, val in mass_components.items():
                    pct = val/total_mass*100
                    st.markdown(f"- {label_mapping[comp]}: {val:.1f} kg ({pct:.1f}%)")
            with col2:
                st.markdown("**体积组成 (L)**" if st.session_state.language=='zh' else "**Volume Composition (L)**")
                for comp, val in volume_components.items():
                    pct = val/total_volume*100
                    st.markdown(f"- {label_mapping[comp]}: {val*1000:.3f} L ({pct:.1f}%)")

# ==================== 标签页3：计算说明 ====================
with tab3:
    st.markdown(f'<h2 class="section-header">{t("calculation_explanation")}</h2>', unsafe_allow_html=True)
    with st.expander("📝 基础能量密度计算步骤" if st.session_state.language=="zh" else "📝 Basic Energy Density Calculation Steps", expanded=True):
        st.markdown(f"### {t('basic_calculation_steps')}")
        st.markdown(f"1. **{t('dehydrogenation_calculation')}**:")
        st.markdown(f"   {t('dehydrogenation_energy')} = ({t('dehydrogenation_enthalpy')} × 500 mol/kg) / 3600 = ({dehydrogenation_enthalpy} kJ/mol × {moles_per_kg_h2} mol/kg) / 3600 = {dehydrogenation_energy_consumption:.2f} kWh/kgH₂")
        st.markdown(f"2. **{t('net_power_calculation')}**:")
        st.markdown(f"   {t('net_power')} = ({t('h2_energy_density')} - {t('dehydrogenation_energy')}) × {t('fuel_cell_utilization')} = ({H2_ENERGY_DENSITY} {t('kwh_kg')} - {dehydrogenation_energy_consumption:.2f} {t('kwh_kg')}) × ({fuel_cell_efficiency:.1f}% / 100) = {net_power_generation:.2f} kWh/kgH₂")
        st.markdown(f"3. **{t('material_energy_density_calculation')}**:")
        st.markdown(f"   {t('material')} {t('mass_energy_density')} = {t('net_power')} / (1 / {t('hydrogen_mass_fraction')}) = {net_power_generation:.2f} kWh/kgH₂ / (1 / {hydrogen_mass_fraction}) = {material_mass_energy_density:.3f} {t('kwh_kg')}")
        st.markdown(f"   {t('material')} {t('volume_energy_density')} = {t('mass_energy_density')} × {t('material_density')} = {material_mass_energy_density:.3f} {t('kwh_kg')} × {material_density} {t('material_density_unit')} = {material_volume_energy_density:.1f} {t('kwh_m3')}")

    if container_shape != t("custom") and container_thickness > 0:
        with st.expander("📐 外壳计算步骤" if st.session_state.language=="zh" else "📐 Shell Calculation Steps", expanded=True):
            st.markdown(f"### {t('shell_calculation_steps')}")
            st.markdown(f"1. **外壳数量分配**:")
            st.markdown(f"   {t('material_volume_required')} = {material_volume_required:.3f} m³, {t('container_count')} = {container_count}, {t('material_per_container')} = {material_volume_required:.3f} m³ / {container_count} = {material_volume_per_container:.3f} m³")
            st.markdown(f"2. **{t('filling_ratio_calculation')}**:")
            st.markdown(f"   {t('internal_volume_required')} (单个外壳) = {t('material_per_container')} / ({t('filling_ratio')} / 100) = {material_volume_per_container:.3f} m³ / ({filling_ratio:.1f}% / 100) = {internal_volume_per_container:.3f} m³")
            if container_shape == t("cylinder"):
                if cylinder_input_mode == t("by_radius"):
                    st.markdown(f"3. **{t('single_shell_dimensions')} ({t('by_radius')})**:")
                    st.markdown(f"   {t('base_area')} = π × {t('container_radius')}² = 3.1416 × ({container_radius} m)² = {base_area:.3f} m²")
                    st.markdown(f"   {t('container_height')} = {t('internal_volume_required')} / {t('base_area')} = {internal_volume_per_container:.3f} m³ / {base_area:.3f} m² = {calculated_container_height:.3f} m")
                elif cylinder_input_mode == t("by_height"):
                    st.markdown(f"3. **{t('single_shell_dimensions')} ({t('by_height')})**:")
                    st.markdown(f"   {t('container_height')} = {container_height_input} m")
                    st.markdown(f"   {t('container_radius')} = √({t('internal_volume_required')} / (π × {t('container_height')})) = √({internal_volume_per_container:.3f} m³ / (3.1416 × {container_height_input} m)) = {calculated_container_radius:.3f} m")
                else:
                    st.markdown(f"3. **{t('single_shell_dimensions')} ({t('minimum_surface')})**:")
                    st.markdown(f"   **最优形状条件**: 圆柱直径 = 高度 (h = 2r)")
                    st.markdown(f"   {t('internal_volume_required')} = π × r² × h = 2πr³ → r = ({t('internal_volume_required')} / (2π))^(1/3) = ({internal_volume_per_container:.3f} m³ / (2×3.1416))^(1/3) = {calculated_container_radius:.3f} m, h = 2r = {calculated_container_height:.3f} m")
                st.markdown(f"4. **{t('single_shell_volume')} {t('calculation')}**:")
                st.markdown(f"   {t('outer_volume')} = {t('base_area')} × {t('container_height')} = {base_area:.3f} m² × {calculated_container_height:.3f} m = {outer_volume:.3f} m³")
                st.markdown(f"   {t('inner_radius')} = {t('container_radius')} - {t('container_thickness')} = {container_radius if container_radius is not None else calculated_container_radius:.3f} m - {container_thickness:.3f} m = {inner_radius:.3f} m")
                st.markdown(f"   {t('inner_volume')} = π × {t('inner_radius')}² × ({t('container_height')} - 2{t('container_thickness')}) = {inner_volume:.3f} m³")
                st.markdown(f"   {t('single_shell_volume')} = {outer_volume:.3f} m³ - {inner_volume:.3f} m³ = {single_shell_volume:.3f} m³")
            else:
                st.markdown(f"3. **{t('single_shell_dimensions')}**:")
                st.markdown(f"   {t('base_area')} = {t('container_length')} × {t('container_width')} = {container_length} m × {container_width} m = {base_area:.3f} m²")
                st.markdown(f"   {t('container_height')} = {t('internal_volume_required')} / {t('base_area')} = {internal_volume_per_container:.3f} m³ / {base_area:.3f} m² = {calculated_container_height:.3f} m")
                st.markdown(f"4. **{t('single_shell_volume')} {t('calculation')}**:")
                st.markdown(f"   {t('outer_volume')} = {t('container_length')} × {t('container_width')} × {t('container_height')} = {container_length} m × {container_width} m × {calculated_container_height:.3f} m = {outer_volume:.3f} m³")
                st.markdown(f"   {t('inner_length')} = {t('container_length')} - 2{t('container_thickness')} = {container_length} m - 2×{container_thickness} m = {inner_length:.3f} m")
                st.markdown(f"   {t('inner_width')} = {t('container_width')} - 2{t('container_thickness')} = {container_width} m - 2×{container_thickness} m = {inner_width:.3f} m")
                st.markdown(f"   {t('inner_height')} = {t('container_height')} - 2{t('container_thickness')} = {calculated_container_height:.3f} m - 2×{container_thickness} m = {inner_height:.3f} m")
                st.markdown(f"   {t('inner_volume')} = {t('inner_length')} × {t('inner_width')} × {t('inner_height')} = {inner_length:.3f} m × {inner_width:.3f} m × {inner_height:.3f} m = {inner_volume:.3f} m³")
                st.markdown(f"   {t('single_shell_volume')} = {outer_volume:.3f} m³ - {inner_volume:.3f} m³ = {single_shell_volume:.3f} m³")
            st.markdown(f"5. **{t('single_shell_mass')} {t('calculation')}**:")
            st.markdown(f"   {t('single_shell_mass')} = {t('single_shell_volume')} × {t('shell_density')} = {single_shell_volume:.3f} m³ × {shell_density} {t('material_density_unit')} = {single_shell_mass:.1f} kg")
            st.markdown(f"6. **{t('total_shell_parameters')} {t('calculation')}**:")
            st.markdown(f"   {t('total_shell_volume')} = {t('single_shell_volume')} × {t('container_count')} = {single_shell_volume:.3f} m³ × {container_count} = {total_shell_volume:.3f} m³")
            st.markdown(f"   {t('total_shell_mass')} = {t('single_shell_mass')} × {t('container_count')} = {single_shell_mass:.1f} kg × {container_count} = {total_shell_mass:.1f} kg")

    with st.expander("🔢 系统能量密度计算步骤" if st.session_state.language=="zh" else "🔢 System Energy Density Calculation Steps", expanded=True):
        st.markdown(f"### {t('system_energy_density_steps')}")
        if use_volume_mode:
            st.markdown(f"1. **总储能能量计算**: 由外壳容积定义，总能量 = {total_energy_required:.1f} kWh")
        else:
            st.markdown(f"1. **{t('total_energy_required')} {t('calculation')}**: {t('total_energy_required')} = {output_power} kW × {endurance_time} h = {total_energy_required:.1f} kWh")
        st.markdown(f"2. **{t('material_requirements')} {t('calculation')}**:")
        st.markdown(f"   {t('material_mass_required')} = {total_energy_required:.1f} kWh / {material_mass_energy_density:.3f} {t('kwh_kg')} = {material_mass_required:.1f} kg")
        st.markdown(f"   {t('material_volume_required')} = {total_energy_required:.1f} kWh / {material_volume_energy_density:.1f} {t('kwh_m3')} = {material_volume_required:.3f} m³")
        st.markdown(f"3. **{t('system_total')} {t('calculation')} ({t('with_shell')})**:")
        if container_thickness > 0 or container_shape == t("custom"):
            st.markdown(f"   {t('system_total_mass')} = {material_mass_required:.1f} kg + {fuel_cell_mass} kg + {total_shell_mass:.1f} kg = {system_total_mass_with_shell:.1f} kg")
            st.markdown(f"   {t('system_total_volume')} = {material_volume_required:.3f} m³ + {fuel_cell_volume/1000:.3f} m³ + {total_shell_volume:.3f} m³ = {system_total_volume_with_shell:.3f} m³")
        else:
            st.markdown(f"   {t('system_total_mass')} = {material_mass_required:.1f} kg + {fuel_cell_mass} kg = {system_total_mass_with_shell:.1f} kg")
            st.markdown(f"   {t('system_total_volume')} = {material_volume_required:.3f} m³ + {fuel_cell_volume/1000:.3f} m³ = {system_total_volume_with_shell:.3f} m³")
        st.markdown(f"4. **{t('system_energy_density')} {t('calculation')} ({t('with_shell')})**:")
        st.markdown(f"   {t('system_mass_energy_density')} = {total_energy_required:.1f} kWh / {system_total_mass_with_shell:.1f} kg = {system_mass_energy_density_with_shell:.3f} {t('kwh_kg')}")
        st.markdown(f"   {t('system_volume_energy_density')} = {total_energy_required:.1f} kWh / {system_total_volume_with_shell:.3f} m³ = {system_volume_energy_density_with_shell:.1f} {t('kwh_m3')}")

# ==================== 标签页4：材料库 ====================
with tab4:
    st.markdown(f'<h2 class="section-header">{t("material_comparison")}</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {t('preset_hydrogen_materials')}")
        material_comparison_data = []
        for material, props in PRESET_MATERIALS.items():
            material_comparison_data.append({t("material"): material, f"{t('dehydrogenation_enthalpy')} ({t('dehydrogenation_enthalpy_unit')})": props["dehydrogenation_enthalpy"], f"{t('material_density')} ({t('material_density_unit')})": props["material_density"], t("hydrogen_mass_fraction"): props["hydrogen_mass_fraction"], t("description"): props["description"][st.session_state.language]})
        st.dataframe(pd.DataFrame(material_comparison_data), width='stretch')
    with col2:
        st.markdown(f"### {t('preset_shell_materials')}")
        shell_material_comparison_data = []
        for material_key, props in PRESET_SHELL_MATERIALS.items():
            shell_material_comparison_data.append({t("material"): props['display_name'][st.session_state.language], f"{t('shell_density')} ({t('material_density_unit')})": props["density"], t("description"): props["description"][st.session_state.language]})
        st.dataframe(pd.DataFrame(shell_material_comparison_data), width='stretch')

# ==================== 标签页5：系统原理 ====================
with tab5:
    st.markdown(f'<h2 class="section-header">{t("system_principle")}</h2>', unsafe_allow_html=True)
    st.markdown(f"### {t('subtitle')}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{t('key_concepts')}**:")
        st.markdown(f"- **{t('material')} {t('volume_energy_density')}**: {t('consider_only_the_energy_density_of_the_hydrogen_storage_material_itself')}")
        st.markdown(f"- **{t('system_energy_density')} ({t('no_shell')})**: {t('actual_energy_density_after_considering_fuel_cell_system_mass_and_volume')}")
        st.markdown(f"- **{t('system_energy_density')} ({t('with_shell')})**: {t('actual_energy_density_further_considering_shell_mass_and_volume')}")
        st.markdown(f"- **{t('dilution_effect')}**: {t('as_endurance_time_increases_system_energy_density_approaches_material_energy_density')}")
        st.markdown(f"- **{t('container_count')}**: {t('help_container_count')}")
    with col2:
        st.markdown(f"**{t('application_significance')}**:")
        st.markdown(f"- {t('short_endurance_applications')}: {t('system_energy_density_is_greatly_affected_by_stack_and_shell')}")
        st.markdown(f"- {t('long_endurance_applications')}: {t('system_energy_density_approaches_material_energy_density')}")
        st.markdown(f"- {t('system_design')}: {t('balance_between_endurance_requirements_system_compactness_and_shell_design')}")
        st.markdown(f"- **多罐设计**: 允许将大容量储氢材料分配到多个较小的罐体中，便于安装、维护和安全设计")
    st.markdown("---")
    st.markdown(f"**{t('calculation_principle')}**: {t('solid_state_hydrogen_storage_material_energy_density_calculation_based_on_dehydrogenation_energy_consumption_fuel_cell_efficiency_system_parameters_and_shell_parameters')}")
    st.markdown(f"**{t('h2_mass_energy_density')}**: {H2_ENERGY_DENSITY} {t('kwh_kg')} ({t('fixed_value')})")
    st.markdown(f"**{t('li_battery_reference')}**: {t('mass_energy_density')} {li_battery_mass_density} {t('kwh_kg')}, {t('volume_energy_density')} {li_battery_volume_density} {t('kwh_m3')}")

# ==================== 标签页6：批量计算与导出 ====================
with tab6:
    st.markdown(f'<h2 class="section-header">{t("batch_export")}</h2>', unsafe_allow_html=True)

    st.markdown(f"**{t('batch_settings')}**")
    col1, col2, col3 = st.columns(3)
    with col1:
        eff_start = st.number_input(t("start_efficiency"), min_value=0.0, max_value=100.0,
                                    value=10.0, step=5.0, key="batch_eff_start")
    with col2:
        eff_end = st.number_input(t("end_efficiency"), min_value=0.0, max_value=100.0,
                                  value=100.0, step=5.0, key="batch_eff_end")
    with col3:
        eff_step = st.number_input(t("step_efficiency"), min_value=0.1, max_value=20.0,
                                   value=10.0, step=1.0, key="batch_eff_step")

    col4, col5, col6 = st.columns(3)
    with col4:
        fr_start = st.number_input(t("start_filling_ratio"), min_value=0.0, max_value=100.0,
                                   value=50.0, step=5.0, key="batch_fr_start")
    with col5:
        fr_end = st.number_input(t("end_filling_ratio"), min_value=0.0, max_value=100.0,
                                 value=100.0, step=5.0, key="batch_fr_end")
    with col6:
        fr_step = st.number_input(t("step_filling_ratio"), min_value=0.1, max_value=20.0,
                                  value=10.0, step=1.0, key="batch_fr_step")

    col7, col8, col9 = st.columns(3)
    with col7:
        et_start = st.number_input(t("start_endurance"), min_value=0.1, max_value=100.0,
                                   value=1.0, step=1.0, key="batch_et_start")
    with col8:
        et_end = st.number_input(t("end_endurance"), min_value=0.1, max_value=100.0,
                                 value=10.0, step=1.0, key="batch_et_end")
    with col9:
        et_step = st.number_input(t("step_endurance"), min_value=0.1, max_value=20.0,
                                  value=1.0, step=0.5, key="batch_et_step")

    all_h2_materials = list(PRESET_MATERIALS.keys())
    selected_h2_materials = st.multiselect(
        t("select_hydrogen_materials"),
        options=all_h2_materials,
        default=all_h2_materials,
        format_func=lambda x: f"{x} - {PRESET_MATERIALS[x]['description'][st.session_state.language]}",
        key="batch_h2_materials"
    )
    if not selected_h2_materials:
        st.warning("请至少选择一种储氢材料！" if st.session_state.language=='zh' else "Please select at least one hydrogen storage material!")

    all_shell_options = list(PRESET_SHELL_MATERIALS.keys())
    shell_display_names = {key: PRESET_SHELL_MATERIALS[key]['display_name'][st.session_state.language] for key in all_shell_options}
    selected_shells = st.multiselect(
        t("select_shell_materials"),
        options=all_shell_options,
        default=all_shell_options,
        format_func=lambda x: shell_display_names[x],
        key="batch_shell_materials"
    )
    if not selected_shells:
        st.warning("请至少选择一种外壳材料！" if st.session_state.language=='zh' else "Please select at least one shell material!")

    FUEL_CELL_PRESETS = [
        {"power_kw": 2.4, "mass_kg": 8.9, "volume_L": 6.384},
        {"power_kw": 3.0, "mass_kg": 10.5, "volume_L": 7.561},
        {"power_kw": 4.8, "mass_kg": 15.3, "volume_L": 11.093},
        {"power_kw": 22.9, "mass_kg": 14.3, "volume_L": 11.628},
        {"power_kw": 27.0, "mass_kg": 11.8, "volume_L": 10.483},
        {"power_kw": 29.3, "mass_kg": 17.2, "volume_L": 14.273},
        {"power_kw": 34.4, "mass_kg": 14.0, "volume_L": 12.798},
        {"power_kw": 34.5, "mass_kg": 19.5, "volume_L": 16.416},
        {"power_kw": 37.0, "mass_kg": 20.7, "volume_L": 17.465},
        {"power_kw": 40.4, "mass_kg": 15.8, "volume_L": 14.633},
        {"power_kw": 43.4, "mass_kg": 16.7, "volume_L": 15.55},
        {"power_kw": 53.9, "mass_kg": 20.0, "volume_L": 18.957},
        {"power_kw": 66.0, "mass_kg": 23.7, "volume_L": 22.452},
        {"power_kw": 71.9, "mass_kg": 25.6, "volume_L": 24.286},
        {"power_kw": 83.9, "mass_kg": 29.3, "volume_L": 27.955},
        {"power_kw": 115.8, "mass_kg": 38.5, "volume_L": 39.033},
    ]
    fc_preset_options = [f"{p['power_kw']} kW / {p['mass_kg']} kg / {p['volume_L']} L" for p in FUEL_CELL_PRESETS]
    selected_fc_indices = st.multiselect(
        t("select_fuel_cell_presets"),
        options=list(range(len(FUEL_CELL_PRESETS))),
        format_func=lambda i: fc_preset_options[i],
        default=[],
        key="batch_fc_presets"
    )
    use_fc_presets = len(selected_fc_indices) > 0

    st.markdown(f"**{t('shape_configuration')}**")
    st.info("勾选要参与批量计算的形状，并设置其几何参数。外壳厚度、罐子数量等通用参数沿用侧边栏的值。")

    shape_configs = []

    with st.expander(t("shape_cylinder_radius")):
        col1, col2 = st.columns(2)
        with col1:
            enabled_rad = st.checkbox(t("enable_shape"), value=True, key="shape_enable_rad")
        with col2:
            radius_mm = st.number_input(t("shape_radius_mm"), min_value=1.0, value=200.0, step=10.0, key="shape_rad_radius")
        shape_configs.append({
            "type": "cylinder_radius",
            "display": t("shape_cylinder_radius"),
            "enabled": enabled_rad,
            "params": {"radius_m": radius_mm / 1000.0}
        })

    with st.expander(t("shape_cylinder_height")):
        col1, col2 = st.columns(2)
        with col1:
            enabled_height = st.checkbox(t("enable_shape"), value=True, key="shape_enable_height")
        with col2:
            height_mm = st.number_input(t("shape_height_mm"), min_value=1.0, value=500.0, step=10.0, key="shape_height_height")
        shape_configs.append({
            "type": "cylinder_height",
            "display": t("shape_cylinder_height"),
            "enabled": enabled_height,
            "params": {"height_m": height_mm / 1000.0}
        })

    with st.expander(t("shape_cylinder_optimal")):
        col1, col2 = st.columns(2)
        with col1:
            enabled_opt = st.checkbox(t("enable_shape"), value=True, key="shape_enable_opt")
        with col2:
            st.markdown("*自动计算直径=高度*")
        shape_configs.append({
            "type": "cylinder_optimal",
            "display": t("shape_cylinder_optimal"),
            "enabled": enabled_opt,
            "params": {}
        })

    with st.expander(t("shape_cuboid")):
        col1, col2 = st.columns(2)
        with col1:
            enabled_cub = st.checkbox(t("enable_shape"), value=True, key="shape_enable_cub")
        with col2:
            len_mm = st.number_input(t("shape_length_mm"), min_value=1.0, value=400.0, step=10.0, key="shape_cub_len")
            wid_mm = st.number_input(t("shape_width_mm"), min_value=1.0, value=300.0, step=10.0, key="shape_cub_wid")
        shape_configs.append({
            "type": "cuboid",
            "display": t("shape_cuboid"),
            "enabled": enabled_cub,
            "params": {"length_m": len_mm / 1000.0, "width_m": wid_mm / 1000.0}
        })

    enabled_shapes = [cfg for cfg in shape_configs if cfg["enabled"]]
    if not enabled_shapes:
        st.warning("请至少启用一种外壳形状！" if st.session_state.language=='zh' else "Please enable at least one shell shape!")

    if st.button(t("start_batch"), type="primary"):
        if not selected_h2_materials or not selected_shells or not enabled_shapes:
            st.error("请确保已选择储氢材料、外壳材料并启用至少一种外壳形状！" if st.session_state.language=='zh' else "Please ensure hydrogen materials, shell materials and at least one shape are selected!")
        else:
            efficiencies = []
            e = eff_start
            while e <= eff_end + 1e-6:
                efficiencies.append(round(e, 1))
                e += eff_step

            filling_ratios = []
            fr = fr_start
            while fr <= fr_end + 1e-6:
                filling_ratios.append(round(fr, 1))
                fr += fr_step

            endurance_times_batch = []
            et = et_start
            while et <= et_end + 1e-6:
                endurance_times_batch.append(round(et, 1))
                et += et_step

            if use_fc_presets:
                fc_params_list = [FUEL_CELL_PRESETS[i] for i in selected_fc_indices]
                fc_display_list = [fc_preset_options[i] for i in selected_fc_indices]
            else:
                fc_params_list = [{
                    "power_kw": st.session_state.output_power,
                    "mass_kg": st.session_state.fuel_cell_mass,
                    "volume_L": st.session_state.fuel_cell_volume
                }]
                fc_display_list = [f"侧边栏设置 ({st.session_state.output_power} kW / {st.session_state.fuel_cell_mass} kg / {st.session_state.fuel_cell_volume} L)"]

            batch_container_count = st.session_state.container_count
            batch_container_thickness = st.session_state.container_thickness

            H2_ENERGY_DENSITY_FIXED = 39.4
            moles_per_kg_h2_fixed = 500

            def compute_shell_volume_and_dimensions(shape_cfg, internal_volume_per_container, thickness_m):
                t = thickness_m
                if shape_cfg["type"] == "cylinder_radius":
                    r = shape_cfg["params"]["radius_m"]
                    base_area = math.pi * r ** 2
                    height = internal_volume_per_container / base_area
                    outer_vol = base_area * height
                    inner_r = r - t
                    if inner_r > 0 and height > 2 * t:
                        inner_vol = math.pi * inner_r ** 2 * (height - 2 * t)
                    else:
                        inner_vol = 0
                    shell_vol = outer_vol - inner_vol
                    dimensions = {"radius_m": r, "height_m": height}
                    return shell_vol, dimensions
                elif shape_cfg["type"] == "cylinder_height":
                    h = shape_cfg["params"]["height_m"]
                    r = math.sqrt(internal_volume_per_container / (math.pi * h))
                    base_area = math.pi * r ** 2
                    outer_vol = base_area * h
                    inner_r = r - t
                    if inner_r > 0 and h > 2 * t:
                        inner_vol = math.pi * inner_r ** 2 * (h - 2 * t)
                    else:
                        inner_vol = 0
                    shell_vol = outer_vol - inner_vol
                    dimensions = {"radius_m": r, "height_m": h}
                    return shell_vol, dimensions
                elif shape_cfg["type"] == "cylinder_optimal":
                    r = (internal_volume_per_container / (2 * math.pi)) ** (1/3)
                    h = 2 * r
                    base_area = math.pi * r ** 2
                    outer_vol = base_area * h
                    inner_r = r - t
                    if inner_r > 0 and h > 2 * t:
                        inner_vol = math.pi * inner_r ** 2 * (h - 2 * t)
                    else:
                        inner_vol = 0
                    shell_vol = outer_vol - inner_vol
                    dimensions = {"radius_m": r, "height_m": h}
                    return shell_vol, dimensions
                elif shape_cfg["type"] == "cuboid":
                    L = shape_cfg["params"]["length_m"]
                    W = shape_cfg["params"]["width_m"]
                    base_area = L * W
                    height = internal_volume_per_container / base_area
                    outer_vol = L * W * height
                    inner_L = L - 2 * t
                    inner_W = W - 2 * t
                    inner_H = height - 2 * t
                    if inner_L > 0 and inner_W > 0 and inner_H > 0:
                        inner_vol = inner_L * inner_W * inner_H
                    else:
                        inner_vol = 0
                    shell_vol = outer_vol - inner_vol
                    dimensions = {"length_m": L, "width_m": W, "height_m": height}
                    return shell_vol, dimensions
                else:
                    return 0.0, {}

            def compute_system_metrics_for_combination(h2_props, shell_density_val, efficiency_pct,
                                                        filling_ratio_pct, shape_cfg, fc_params, endurance_time_h):
                fc_power = fc_params["power_kw"]
                fc_mass = fc_params["mass_kg"]
                fc_volume_L = fc_params["volume_L"]

                de_en = (h2_props["dehydrogenation_enthalpy"] * moles_per_kg_h2_fixed) / 3600
                net_power_per_kg_h2 = (H2_ENERGY_DENSITY_FIXED - de_en) * (efficiency_pct / 100.0)
                material_mass_ed = net_power_per_kg_h2 / (1.0 / h2_props["hydrogen_mass_fraction"])
                material_volume_ed = material_mass_ed * h2_props["material_density"]
                total_energy = fc_power * endurance_time_h
                material_mass_req = total_energy / material_mass_ed
                material_volume_req = total_energy / material_volume_ed

                dimensions_info = {}

                if batch_container_thickness == 0:
                    total_mass = material_mass_req + fc_mass
                    total_volume = material_volume_req + (fc_volume_L / 1000.0)
                    system_mass_ed = total_energy / total_mass
                    system_volume_ed = total_energy / total_volume
                    return {
                        "system_mass_ed": system_mass_ed,
                        "system_volume_ed": system_volume_ed,
                        "material_mass_req": material_mass_req,
                        "material_volume_req": material_volume_req,
                        "total_mass": total_mass,
                        "total_volume": total_volume,
                        "dimensions": dimensions_info
                    }

                material_volume_per_container = material_volume_req / batch_container_count
                internal_volume_per_container = material_volume_per_container / (filling_ratio_pct / 100.0)

                single_shell_vol, dimensions_info = compute_shell_volume_and_dimensions(
                    shape_cfg, internal_volume_per_container, batch_container_thickness
                )
                single_shell_mass = single_shell_vol * shell_density_val
                total_shell_vol = single_shell_vol * batch_container_count
                total_shell_mass = single_shell_mass * batch_container_count

                total_mass = material_mass_req + fc_mass + total_shell_mass
                total_volume = material_volume_req + (fc_volume_L / 1000.0) + total_shell_vol
                system_mass_ed = total_energy / total_mass
                system_volume_ed = total_energy / total_volume

                return {
                    "system_mass_ed": system_mass_ed,
                    "system_volume_ed": system_volume_ed,
                    "material_mass_req": material_mass_req,
                    "material_volume_req": material_volume_req,
                    "total_mass": total_mass,
                    "total_volume": total_volume,
                    "dimensions": dimensions_info
                }

            performance_results = []
            dimensions_results = []

            total_combinations = (len(selected_h2_materials) * len(selected_shells) *
                                  len(efficiencies) * len(filling_ratios) *
                                  len(enabled_shapes) * len(fc_params_list) *
                                  len(endurance_times_batch))
            progress_bar = st.progress(0, text="批量计算中..." if st.session_state.language=='zh' else "Batch calculation...")
            idx = 0

            for h2_key in selected_h2_materials:
                h2_props = PRESET_MATERIALS[h2_key]
                h2_display = f"{h2_key} - {h2_props['description'][st.session_state.language]}"
                for shell_key in selected_shells:
                    shell_density_val = PRESET_SHELL_MATERIALS[shell_key]["density"]
                    shell_display = PRESET_SHELL_MATERIALS[shell_key]['display_name'][st.session_state.language]
                    for eff in efficiencies:
                        for fr in filling_ratios:
                            for shape_cfg in enabled_shapes:
                                for fc_idx, fc_params in enumerate(fc_params_list):
                                    for et in endurance_times_batch:
                                        metrics = compute_system_metrics_for_combination(
                                            h2_props, shell_density_val, eff, fr, shape_cfg, fc_params, et
                                        )
                                        performance_results.append({
                                            t("hydrogen_material_name"): h2_display,
                                            t("shell_material_name"): shell_display,
                                            "外壳形状": shape_cfg["display"],
                                            t("fuel_cell_model"): fc_display_list[fc_idx],
                                            t("endurance_h"): et,
                                            t("efficiency"): eff,
                                            t("filling_ratio"): fr,
                                            t("mass_energy_density_system"): metrics["system_mass_ed"],
                                            t("volume_energy_density_system"): metrics["system_volume_ed"],
                                            t("material_mass_required"): metrics["material_mass_req"],
                                            t("material_volume_required"): metrics["material_volume_req"],
                                            t("total_system_mass_batch"): metrics["total_mass"],
                                            t("total_system_volume_batch"): metrics["total_volume"] * 1000
                                        })
                                        dims = metrics["dimensions"]
                                        dim_record = {
                                            t("hydrogen_material_name"): h2_display,
                                            t("shell_material_name"): shell_display,
                                            "外壳形状": shape_cfg["display"],
                                            t("fuel_cell_model"): fc_display_list[fc_idx],
                                            t("endurance_h"): et,
                                            t("efficiency"): eff,
                                            t("filling_ratio"): fr,
                                        }
                                        if shape_cfg["type"] in ["cylinder_radius", "cylinder_height", "cylinder_optimal"]:
                                            dim_record[t("shape_radius_m")] = dims.get("radius_m", None)
                                            dim_record[t("shape_height_m")] = dims.get("height_m", None)
                                        elif shape_cfg["type"] == "cuboid":
                                            dim_record[t("shape_length_m")] = dims.get("length_m", None)
                                            dim_record[t("shape_width_m")] = dims.get("width_m", None)
                                            dim_record[t("shape_height_m")] = dims.get("height_m", None)
                                        dimensions_results.append(dim_record)

                                        idx += 1
                                        progress_bar.progress(idx / total_combinations)

            df_performance = pd.DataFrame(performance_results)
            df_dimensions = pd.DataFrame(dimensions_results)

            st.markdown(f"### {t('batch_results')}")
            st.dataframe(df_performance, use_container_width=True)

            st.markdown(f"### {t('shell_dimensions_table')}")
            if not df_dimensions.empty:
                st.dataframe(df_dimensions, use_container_width=True)
            else:
                st.info("无外壳厚度为零或未产生尺寸数据，尺寸表为空。")

            col_csv1, col_csv2 = st.columns(2)
            with col_csv1:
                csv_perf = df_performance.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label=t("download_csv"),
                    data=csv_perf,
                    file_name="batch_performance.csv",
                    mime="text/csv",
                    key="download_perf"
                )
            with col_csv2:
                if not df_dimensions.empty:
                    csv_dim = df_dimensions.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        label=t("download_dimensions_csv"),
                        data=csv_dim,
                        file_name="batch_dimensions.csv",
                        mime="text/csv",
                        key="download_dim"
                    )

            st.success(f"计算完成！共生成 {len(performance_results)} 条性能记录，{len(dimensions_results)} 条尺寸记录。" if st.session_state.language=='zh' else f"Calculation completed! {len(performance_results)} performance records and {len(dimensions_results)} dimension records generated.")
