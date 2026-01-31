import request from "@/utils/request";

const API_PATH = "/resource/data";

const ResourceDataAPI = {
  // 列表查询
  listResourceData(query: ResourceDataPageQuery) {
    return request<ApiResponse<PageResult<ResourceDataTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailResourceData(id: number) {
    return request<ApiResponse<ResourceDataTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createResourceData(body: ResourceDataForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateResourceData(id: number, body: ResourceDataForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteResourceData(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchResourceData(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportResourceData(query: ResourceDataPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateResourceData() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importResourceData(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default ResourceDataAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface ResourceDataPageQuery extends PageQuery {
  name?: string;
  type?: string;
  format?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface ResourceDataTable extends BaseType {
  name?: string;
  type?: string;
  format?: string;
  local_path?: string;
  network_url?: string;
  cloud_url?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface ResourceDataForm extends BaseFormType {
  name?: string;
  type?: string;
  format?: string;
  local_path?: string;
  network_url?: string;
  cloud_url?: string;
}
