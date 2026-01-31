import request from "@/utils/request";

const API_PATH = "/resource/author";

const ResourceAuthorAPI = {
  // 列表查询
  listResourceAuthor(query: ResourceAuthorPageQuery) {
    return request<ApiResponse<PageResult<ResourceAuthorTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailResourceAuthor(id: number) {
    return request<ApiResponse<ResourceAuthorTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createResourceAuthor(body: ResourceAuthorForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateResourceAuthor(id: number, body: ResourceAuthorForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteResourceAuthor(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchResourceAuthor(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportResourceAuthor(query: ResourceAuthorPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateResourceAuthor() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importResourceAuthor(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default ResourceAuthorAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface ResourceAuthorPageQuery extends PageQuery {
  name?: string;
  institution?: string;
  email?: string;
  orcid?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface ResourceAuthorTable extends BaseType {
  name?: string;
  institution?: string;
  email?: string;
  orcid?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface ResourceAuthorForm extends BaseFormType {
  name?: string;
  institution?: string;
  email?: string;
  orcid?: string;
}
