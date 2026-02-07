import request from "@/utils/request";

const API_PATH = "/plot/sample";

const PlotSampleAPI = {
  // 列表查询
  listPlotSample(query: PlotSamplePageQuery) {
    return request<ApiResponse<PageResult<PlotSampleTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailPlotSample(id: number) {
    return request<ApiResponse<PlotSampleTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createPlotSample(body: PlotSampleForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updatePlotSample(id: number, body: PlotSampleForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deletePlotSample(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchPlotSample(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportPlotSample(query: PlotSamplePageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplatePlotSample() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importPlotSample(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default PlotSampleAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface PlotSamplePageQuery extends PageQuery {
  order?: number;
  description?: string;
  script_id?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface PlotSampleTable extends BaseType {
  order?: number;
  script_id?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface PlotSampleForm extends BaseFormType {
  order?: number;
  script_id?: string;
}
