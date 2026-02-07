import { store } from "@/store";
import LabPlotAPI, { LabPlotTable } from "@/api/module_lab/plot";
import { ref, computed, reactive, toRefs } from "vue";

// 类型定义
export interface PlotData  extends LabPlotTable {}


export interface UploadData {
  files: File[];
  options: Record<string, any>;
  status: "idle" | "uploading" | "success" | "error";
  progress: number;
}

export interface HistoricalResult {
  id: number;
  title: string;
  content: string;
  createTime: string;
}

export interface PlotResult {
  imageUrl: string;
  data: any[];
  statistics: Record<string, any>;
  status: "idle" | "processing" | "success" | "error";
  // 新增结果详情数据
  statDescription?: any[];
  outlierAnalysis?: any[];
  normalityTest?: any[];
  tTestResults?: any[];
  statMethod?: string;
}

export interface PlotParams {
  // 统计方法
  statMethod: string;
  groupComparison: string[];
  significanceType: string;
  significanceSize: string;
  groupSpacing: string;
  
  // 点样式
  pointFillColor1: string;
  pointFillColor2: string;
  pointStrokeColor1: string;
  pointStrokeColor2: string;
  pointStyle: string;
  pointSize: string;
  pointOpacity: string;
  
  // 线样式
  lineColor: string;
  lineType: string;
  lineWidth: string;
  
  // 箱线图
  showBox: boolean;
  boxFillColor1: string;
  boxFillColor2: string;
  boxStrokeColor1: string;
  boxStrokeColor2: string;
  boxStrokeWidth: string;
  boxOpacity: string;
  boxWidth: string;
  
  // 标题和标签
  mainTitle: string;
  xAxisTitle: string;
  yAxisTitle: string;
  showLegend: boolean;
  legendTitle: string;
  legendPosition: string;
  xAxisLabels: string;
  xAxisRotation: string;
  yAxisRange: string;
  
  // 其他设置
  showBorder: boolean;
  showGrid: boolean;
  swapAxes: boolean;
  fontSize: string;
  imageWidth: string;
  imageHeight: string;
  fontFamily: string;
}

export const usePlotStore = defineStore(
  "plot",
  () => {
    // 当前绘图详情数据
    const currentPlot = ref<PlotData | null>(null);
    
    // 上传数据
    const uploadData = reactive<UploadData>({
      files: [],
      options: {},
      status: "idle",
      progress: 0,
    });
    
    // 绘图结果
    const plotResult = reactive<PlotResult>({
      imageUrl: "",
      data: [],
      statistics: {},
      status: "idle",
      statDescription: [],
      outlierAnalysis: [],
      normalityTest: [],
      tTestResults: [],
      statMethod: "t-test",
    });
    
    // 历史结果列表
    const historicalResults = ref<HistoricalResult[]>([
      { id: 1, title: "结果1-样本分析", content: "样本A检测阳性，匹配度98.5%", createTime: "2026-02-06 10:00" },
      { id: 2, title: "结果2-样本分析", content: "样本B检测阴性，匹配度95.2%", createTime: "2026-02-06 10:05" },
      { id: 3, title: "结果3-样本分析", content: "样本C检测弱阳性，匹配度89.7%", createTime: "2026-02-06 10:10" },
      { id: 4, title: "结果4-样本分析", content: "样本D检测阳性，匹配度99.1%", createTime: "2026-02-06 10:15" },
      { id: 5, title: "结果5-样本分析", content: "样本E检测阴性，匹配度96.8%", createTime: "2026-02-06 10:20" },
      { id: 6, title: "结果6-样本分析", content: "样本F检测阳性，匹配度97.3%", createTime: "2026-02-06 10:25" },
      { id: 7, title: "结果7-样本分析", content: "样本G检测弱阳性，匹配度88.9%", createTime: "2026-02-06 10:30" },
      { id: 8, title: "结果8-样本分析", content: "样本H检测阴性，匹配度94.5%", createTime: "2026-02-06 10:35" },
      { id: 9, title: "结果9-样本分析", content: "样本I检测阳性，匹配度98.2%", createTime: "2026-02-06 10:40" },
    ]);
    
    // 绘图参数
    const plotParams = reactive<PlotParams>({
      // 统计方法
      statMethod: "t-test",
      groupComparison: ["before_after"],
      significanceType: "star",
      significanceSize: "6pt",
      groupSpacing: "0.5",
      
      // 点样式
      pointFillColor1: "#4DBBD5",
      pointFillColor2: "#E64B35",
      pointStrokeColor1: "#4DBBD5",
      pointStrokeColor2: "#E64B35",
      pointStyle: "circle",
      pointSize: "4",
      pointOpacity: "1",
      
      // 线样式
      lineColor: "#000000",
      lineType: "solid",
      lineWidth: "0.75pt",
      
      // 箱线图
      showBox: true,
      boxFillColor1: "#4DBBD5",
      boxFillColor2: "#E64B35",
      boxStrokeColor1: "#000000",
      boxStrokeColor2: "#000000",
      boxStrokeWidth: "0.75pt",
      boxOpacity: "1",
      boxWidth: "0.5",
      
      // 标题和标签
      mainTitle: "",
      xAxisTitle: "",
      yAxisTitle: "",
      showLegend: true,
      legendTitle: "",
      legendPosition: "default",
      xAxisLabels: "Before, After",
      xAxisRotation: "0",
      yAxisRange: "",
      
      // 其他设置
      showBorder: false,
      showGrid: false,
      swapAxes: false,
      fontSize: "7pt",
      imageWidth: "",
      imageHeight: "",
      fontFamily: "Arial",
    });
    
    // 活动标签页
    const activeTab = ref("main");
    
    // 标签页列表
    const tabs = ref([
      { id: "main", label: "主要结果" },
      { id: "supplementary", label: "补充结果" },
      { id: "methodology", label: "方法学" },
    ]);
    
    // 折叠面板状态
    const activeCollapse = ref(["statistics", "points", "lines", "box", "titles"]);
    
    // 计算属性
    const plotId = computed(() => currentPlot.value?.id);
    const plotName = computed(() => currentPlot.value?.name);
    const hasData = computed(() => uploadData.files.length > 0);
    const isProcessing = computed(() => plotResult.status === "processing");
    const hasResult = computed(() => plotResult.status === "success");
    const statMethodLabel = computed(() => {
      const methods: Record<string, string> = {
        "t-test": "配对样本T检验",
        wilcoxon: "Wilcoxon signed rank test",
        auto: "auto",
      };
      return methods[plotParams.statMethod] || "配对样本T检验";
    });
    
    // 获取绘图详情
    const fetchPlotDetail = async (id: number) => {
      try {
        if (!id || isNaN(id) || id <= 0) {
          currentPlot.value = null;
          return;
        }
        
        const res = await LabPlotAPI.detailLabPlot(id);
        if (res?.data?.data) {
          currentPlot.value = res.data.data;
          console.log("Plot detail loaded:", currentPlot.value);
        } else {
          currentPlot.value = null;
        }
      } catch (error) {
        console.error("Failed to fetch plot detail:", error);
        currentPlot.value = null;
      }
    };
    
    // 更新上传数据
    const updateUploadData = (data: Partial<UploadData>) => {
      Object.assign(uploadData, data);
    };
    
    // 添加上传文件
    const addUploadFiles = (files: File[]) => {
      uploadData.files = [...uploadData.files, ...files];
    };
    
    // 移除上传文件
    const removeUploadFile = (index: number) => {
      uploadData.files.splice(index, 1);
    };
    
    // 清空上传数据
    const clearUploadData = () => {
      Object.assign(uploadData, {
        files: [],
        options: {},
        status: "idle",
        progress: 0,
      });
    };
    
    // 更新绘图参数
    const updatePlotParams = (params: Partial<PlotParams>) => {
      Object.assign(plotParams, params);
    };
    
    // 重置绘图参数
    const resetPlotParams = () => {
      Object.assign(plotParams, {
        statMethod: "t-test",
        groupComparison: ["before_after"],
        significanceType: "star",
        significanceSize: "6pt",
        groupSpacing: "0.5",
        pointFillColor1: "#4DBBD5",
        pointFillColor2: "#E64B35",
        pointStrokeColor1: "#4DBBD5",
        pointStrokeColor2: "#E64B35",
        pointStyle: "circle",
        pointSize: "4",
        pointOpacity: "1",
        lineColor: "#000000",
        lineType: "solid",
        lineWidth: "0.75pt",
        showBox: true,
        boxFillColor1: "#4DBBD5",
        boxFillColor2: "#E64B35",
        boxStrokeColor1: "#000000",
        boxStrokeColor2: "#000000",
        boxStrokeWidth: "0.75pt",
        boxOpacity: "1",
        boxWidth: "0.5",
        mainTitle: "",
        xAxisTitle: "",
        yAxisTitle: "",
        showLegend: true,
        legendTitle: "",
        legendPosition: "default",
        xAxisLabels: "Before, After",
        xAxisRotation: "0",
        yAxisRange: "",
        showBorder: false,
        showGrid: false,
        swapAxes: false,
        fontSize: "7pt",
        imageWidth: "",
        imageHeight: "",
        fontFamily: "Arial",
      });
    };
    
    // 更新绘图结果
    const updatePlotResult = (result: Partial<PlotResult>) => {
      Object.assign(plotResult, result);
    };
    
    // 执行绘图计算
    const executePlot = async () => {
      if (!currentPlot.value || uploadData.files.length === 0) {
        return;
      }
      
      try {
        plotResult.status = "processing";
        
        // 模拟API调用延迟
        await new Promise((resolve) => setTimeout(resolve, 2000));
        
        // 模拟结果数据
        Object.assign(plotResult, {
          imageUrl: "https://via.placeholder.com/800x400/4DBBD5/FFFFFF?text=配对图+示例",
          data: [
            { x: 1, y: 10, category: "A" },
            { x: 2, y: 20, category: "A" },
            { x: 3, y: 15, category: "B" },
            { x: 4, y: 25, category: "B" },
            { x: 5, y: 30, category: "C" },
          ],
          statistics: {
            mean: 20,
            median: 20,
            stdDev: 8.37,
            min: 10,
            max: 30,
          },
          statDescription: [
            {
              group: "Before",
              count: 10,
              min: 172.4,
              max: 235,
              median: 197.35,
              iqr: 19.15,
              q1: 187.8,
              q3: 206.95,
              mean: 200.56,
              sd: 20.028,
              se: 6.3335,
            },
            {
              group: "After",
              count: 10,
              min: 337,
              max: 445.8,
              median: 405,
              iqr: 28.3,
              q1: 384.53,
              q3: 412.83,
              mean: 400.04,
              sd: 30.087,
              se: 9.5143,
            },
          ],
          outlierAnalysis: [
            { group: "After", outliers: "337", anomalies: "" },
          ],
          normalityTest: [
            { df: 9, statistic: 0.96751, pValue: 0.8669 },
          ],
          tTestResults: [
            {
              groupI: "Before",
              groupJ: "After",
              df: 9,
              tStatistic: 25.546,
              difference: 199.48,
              confidenceInterval: "181.82 – 217.14",
              pValue: "1.04e-09",
            },
          ],
          statMethod: plotParams.statMethod,
          status: "success",
        });
        
        console.log("Plot execution completed:", plotResult);
      } catch (error) {
        console.error("Plot execution failed:", error);
        plotResult.status = "error";
      }
    };
    
    // 添加历史结果
    const addHistoricalResult = (result: Omit<HistoricalResult, "id">) => {
      const newId = historicalResults.value.length > 0 
        ? Math.max(...historicalResults.value.map(r => r.id)) + 1 
        : 1;
      historicalResults.value.push({
        id: newId,
        ...result,
      });
    };
    
    // 删除历史结果
    const removeHistoricalResult = (id: number) => {
      const index = historicalResults.value.findIndex(r => r.id === id);
      if (index !== -1) {
        historicalResults.value.splice(index, 1);
      }
    };
    
    // 清空历史结果
    const clearHistoricalResults = () => {
      historicalResults.value = [];
    };
    
    // 切换标签页
    const setActiveTab = (tabId: string) => {
      activeTab.value = tabId;
    };
    
    // 保存结果
    const saveResult = () => {
      console.log("保存结果...");
      // 这里应该调用API保存结果
    };
    
    // 重置所有数据
    const resetAll = () => {
      currentPlot.value = null;
      clearUploadData();
      updatePlotResult({
        imageUrl: "",
        data: [],
        statistics: {},
        status: "idle",
        statDescription: [],
        outlierAnalysis: [],
        normalityTest: [],
        tTestResults: [],
        statMethod: "t-test",
      });
      resetPlotParams();
    };
    
    // 清理数据（用于用户退出或切换）
    const clearPlotData = () => {
      resetAll();
    };
    
    return {
      // 状态
      currentPlot,
      uploadData,
      plotResult,
      historicalResults,
      plotParams,
      activeTab,
      tabs,
      activeCollapse,
      
      // 计算属性
      plotId,
      plotName,
      hasData,
      isProcessing,
      hasResult,
      statMethodLabel,
      
      // 方法
      fetchPlotDetail,
      updateUploadData,
      addUploadFiles,
      removeUploadFile,
      clearUploadData,
      updatePlotParams,
      resetPlotParams,
      updatePlotResult,
      executePlot,
      addHistoricalResult,
      removeHistoricalResult,
      clearHistoricalResults,
      setActiveTab,
      saveResult,
      resetAll,
      clearPlotData,
    };
  },
  {
    persist: true,
  }
);

// 导出 hook 函数
export function usePlotStoreHook() {
  return usePlotStore(store);
}