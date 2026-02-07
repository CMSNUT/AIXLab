import request from "@/utils/request";

const API_PATH = "/plot/method";

const PlotMethodAPI = {
  // 列表查询
  listPlotMethod(query: PlotMethodPageQuery) {
    return request<ApiResponse<PageResult<PlotMethodTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailPlotMethod(id: number) {
    return request<ApiResponse<PlotMethodTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createPlotMethod(body: PlotMethodForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updatePlotMethod(id: number, body: PlotMethodForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deletePlotMethod(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchPlotMethod(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportPlotMethod(query: PlotMethodPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplatePlotMethod() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importPlotMethod(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default PlotMethodAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface PlotMethodPageQuery extends PageQuery {
  description?: string;
  order?: number;
  script_id?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface PlotMethodTable extends BaseType {
  order?: number;
  script_id?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface PlotMethodForm extends BaseFormType {
  order?: number;
  script_id?: string;
}
