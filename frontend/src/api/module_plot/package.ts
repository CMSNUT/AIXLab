import request from "@/utils/request";

const API_PATH = "/plot/package";

const PlotPackageAPI = {
  // 列表查询
  listPlotPackage(query: PlotPackagePageQuery) {
    return request<ApiResponse<PageResult<PlotPackageTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailPlotPackage(id: number) {
    return request<ApiResponse<PlotPackageTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createPlotPackage(body: PlotPackageForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updatePlotPackage(id: number, body: PlotPackageForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deletePlotPackage(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchPlotPackage(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportPlotPackage(query: PlotPackagePageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplatePlotPackage() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importPlotPackage(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default PlotPackageAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface PlotPackagePageQuery extends PageQuery {
  version?: string;
  script_id?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface PlotPackageTable extends BaseType {
  version?: string;
  script_id?: string;
  url?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface PlotPackageForm extends BaseFormType {
  version?: string;
  script_id?: string;
  url?: string;
}
