import request from "@/utils/request";

const API_PATH = "/resource/script";

const ResourceScriptAPI = {
  // 列表查询
  listResourceScript(query: ResourceScriptPageQuery) {
    return request<ApiResponse<PageResult<ResourceScriptTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailResourceScript(id: number) {
    return request<ApiResponse<ResourceScriptTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createResourceScript(body: ResourceScriptForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateResourceScript(id: number, body: ResourceScriptForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteResourceScript(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchResourceScript(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportResourceScript(query: ResourceScriptPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateResourceScript() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importResourceScript(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default ResourceScriptAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface ResourceScriptPageQuery extends PageQuery {
  name?: string;
  type?: string;
  language?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface ResourceScriptTable extends BaseType {
  name?: string;
  type?: string;
  language?: string;
  local_path?: string;
  network_url?: string;
  cloud_url?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface ResourceScriptForm extends BaseFormType {
  name?: string;
  type?: string;
  language?: string;
  local_path?: string;
  network_url?: string;
  cloud_url?: string;
}
