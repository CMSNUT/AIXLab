import request from "@/utils/request";

const API_PATH = "/plot/category";

const PlotCategoryAPI = {
  // 列表查询
  listPlotCategory(query: PlotCategoryPageQuery) {
    return request<ApiResponse<PageResult<PlotCategoryTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailPlotCategory(id: number) {
    return request<ApiResponse<PlotCategoryTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createPlotCategory(body: PlotCategoryForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updatePlotCategory(id: number, body: PlotCategoryForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deletePlotCategory(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchPlotCategory(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportPlotCategory(query: PlotCategoryPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplatePlotCategory() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importPlotCategory(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default PlotCategoryAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface PlotCategoryPageQuery extends PageQuery {
  name?: string;
  code?: string;
  category?: string;
  subcategory?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface PlotCategoryTable extends BaseType {
  name?: string;
  code?: string;
  category?: string;
  subcategory?: string;
  image?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface PlotCategoryForm extends BaseFormType {
  name?: string;
  code?: string;
  category?: string;
  subcategory?: string;
  image?: string;
}
