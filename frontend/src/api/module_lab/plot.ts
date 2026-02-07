import request from "@/utils/request";

const API_PATH = "/lab/plot";

const LabPlotAPI = {
  // 列表查询
  listLabPlot(query: LabPlotPageQuery) {
    return request<ApiResponse<PageResult<LabPlotTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailLabPlot(id: number) {
    return request<ApiResponse<LabPlotTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createLabPlot(body: LabPlotForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateLabPlot(id: number, body: LabPlotForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteLabPlot(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchLabPlot(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportLabPlot(query: LabPlotPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateLabPlot() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importLabPlot(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  // 加法
  add(params: { a: number, b: number }) {
    return request<ApiResponse>({
    // return request ({
      url: `${API_PATH}/add`,
      method: "post",
      headers: { 'Content-Type': 'application/json' },
      // 参数格式保持不变，让中间端处理格式转换
      data: params,
    });
  },

  
};

export default LabPlotAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface LabPlotPageQuery extends PageQuery {
  name?: string;
  code?: string;
  field?: string;
  category?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface LabPlotTable extends BaseType {
  name?: string;
  code?: string;
  field?: string;
  category?: string;
  image?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface LabPlotForm extends BaseFormType {
  name?: string;
  code?: string;
  field?: string;
  category?: string;
  image?: string;
}
