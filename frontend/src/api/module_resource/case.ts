import request from "@/utils/request";

const API_PATH = "/resource/case";

const ResourceCaseAPI = {
  // 列表查询
  listResourceCase(query: ResourceCasePageQuery) {
    return request<ApiResponse<PageResult<ResourceCaseTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailResourceCase(id: number) {
    return request<ApiResponse<ResourceCaseTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createResourceCase(body: ResourceCaseForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateResourceCase(id: number, body: ResourceCaseForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteResourceCase(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchResourceCase(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportResourceCase(query: ResourceCasePageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateResourceCase() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importResourceCase(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default ResourceCaseAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface ResourceCasePageQuery extends PageQuery {
  name?: string;
  description?: string;
  content?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface ResourceCaseTable extends BaseType {
  name?: string;
  content?: string;
  paper_id?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface ResourceCaseForm extends BaseFormType {
  name?: string;
  content?: string;
  paper_id?: string;
}
