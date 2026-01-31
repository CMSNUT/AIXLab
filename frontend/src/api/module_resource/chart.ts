import request from "@/utils/request";

const API_PATH = "/resource/chart";

const ResourceChartAPI = {
  // 列表查询
  listResourceChart(query: ResourceChartPageQuery) {
    return request<ApiResponse<PageResult<ResourceChartTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailResourceChart(id: number) {
    return request<ApiResponse<ResourceChartTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createResourceChart(body: ResourceChartForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateResourceChart(id: number, body: ResourceChartForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteResourceChart(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchResourceChart(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportResourceChart(query: ResourceChartPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateResourceChart() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importResourceChart(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default ResourceChartAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface ResourceChartPageQuery extends PageQuery {
  name?: string;
  code?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface ResourceChartTable extends BaseType {
  paper_id?: string;
  name?: string;
  code?: string;
  local_path?: string;
  network_url?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface ResourceChartForm extends BaseFormType {
  paper_id?: string;
  name?: string;
  code?: string;
  local_path?: string;
  network_url?: string;
}
