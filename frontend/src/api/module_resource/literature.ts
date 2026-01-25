import request from "@/utils/request";

const API_PATH = "/resource/literature";

const ResourceLiteratureAPI = {
  // 列表查询
  listResourceLiterature(query: ResourceLiteraturePageQuery) {
    return request<ApiResponse<PageResult<ResourceLiteratureTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailResourceLiterature(id: number) {
    return request<ApiResponse<ResourceLiteratureTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createResourceLiterature(body: ResourceLiteratureForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateResourceLiterature(id: number, body: ResourceLiteratureForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteResourceLiterature(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchResourceLiterature(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportResourceLiterature(query: ResourceLiteraturePageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateResourceLiterature() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importResourceLiterature(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default ResourceLiteratureAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface ResourceLiteraturePageQuery extends PageQuery {
  status?: string;
  title?: string;
  abstract?: string;
  keywords?: string;
  doi?: string;
  publish_year?: string;
  journal_name?: string;
  volume?: string;
  issue?: string;
  pages?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface ResourceLiteratureTable extends BaseType {
  title?: string;
  abstract?: string;
  keywords?: string;
  doi?: string;
  publish_year?: string;
  journal_name?: string;
  volume?: string;
  issue?: string;
  pages?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface ResourceLiteratureForm extends BaseFormType {
  title?: string;
  abstract?: string;
  keywords?: string;
  doi?: string;
  publish_year?: string;
  journal_name?: string;
  volume?: string;
  issue?: string;
  pages?: string;
}
