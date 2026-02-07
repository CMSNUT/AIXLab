import request from "@/utils/request";

const API_PATH = "/plot/output";

const PlotOutputAPI = {
  // 列表查询
  listPlotOutput(query: PlotOutputPageQuery) {
    return request<ApiResponse<PageResult<PlotOutputTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailPlotOutput(id: number) {
    return request<ApiResponse<PlotOutputTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createPlotOutput(body: PlotOutputForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updatePlotOutput(id: number, body: PlotOutputForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deletePlotOutput(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchPlotOutput(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportPlotOutput(query: PlotOutputPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplatePlotOutput() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importPlotOutput(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default PlotOutputAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface PlotOutputPageQuery extends PageQuery {
  order?: number;
  name?: string;
  description?: string;
  script_id?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface PlotOutputTable extends BaseType {
  order?: number;
  name?: string;
  script_id?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface PlotOutputForm extends BaseFormType {
  order?: number;
  name?: string;
  script_id?: string;
}
