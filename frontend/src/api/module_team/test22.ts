import request from "@/utils/request";

const API_PATH = "/team/test22";

const TeamTest22API = {
  // 列表查询
  listTeamTest22(query: TeamTest22PageQuery) {
    return request<ApiResponse<PageResult<TeamTest22Table[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailTeamTest22(id: number) {
    return request<ApiResponse<TeamTest22Table>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createTeamTest22(body: TeamTest22Form) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateTeamTest22(id: number, body: TeamTest22Form) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteTeamTest22(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchTeamTest22(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportTeamTest22(query: TeamTest22PageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateTeamTest22() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importTeamTest22(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default TeamTest22API;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface TeamTest22PageQuery extends PageQuery {
  name?: string;
  content?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface TeamTest22Table extends BaseType {
  name?: string;
  content?: string;
  file_path?: string;
  image_path?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface TeamTest22Form extends BaseFormType {
  name?: string;
  content?: string;
  file_path?: string;
  image_path?: string;
}
