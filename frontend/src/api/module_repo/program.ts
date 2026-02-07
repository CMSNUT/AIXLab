import request from "@/utils/request";

const API_PATH = "/repo/program";

const RepoProgramAPI = {
  // 列表查询
  listRepoProgram(query: RepoProgramPageQuery) {
    return request<ApiResponse<PageResult<RepoProgramTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailRepoProgram(id: number) {
    return request<ApiResponse<RepoProgramTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createRepoProgram(body: RepoProgramForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateRepoProgram(id: number, body: RepoProgramForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteRepoProgram(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchRepoProgram(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportRepoProgram(query: RepoProgramPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateRepoProgram() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importRepoProgram(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default RepoProgramAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface RepoProgramPageQuery extends PageQuery {
  name?: string;
  alias?: string;
  language?: string;
  field?: string;
  category?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface RepoProgramTable extends BaseType {
  name?: string;
  alias?: string;
  language?: string;
  field?: string;
  category?: string;
  local_file?: string;
  url_link?: string;
  cloud_link?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface RepoProgramForm extends BaseFormType {
  name?: string;
  alias?: string;
  language?: string;
  field?: string;
  category?: string;
  local_file?: string;
  url_link?: string;
  cloud_link?: string;
}
