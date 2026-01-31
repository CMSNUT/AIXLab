import request from "@/utils/request";

const API_PATH = "/team/test";

const TeamTestAPI = {
  // 列表查询
  listTeamTest(query: TeamTestPageQuery) {
    return request<ApiResponse<PageResult<TeamTestTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailTeamTest(id: number) {
    return request<ApiResponse<TeamTestTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createTeamTest(body: TeamTestForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateTeamTest(id: number, body: TeamTestForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteTeamTest(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchTeamTest(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportTeamTest(query: TeamTestPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateTeamTest() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importTeamTest(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default TeamTestAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface TeamTestPageQuery extends PageQuery {
  name?: string;
  content?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface TeamTestTable extends BaseType {
  name?: string;
  content?: string;
  file_path?: string;
  imgage_path?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface TeamTestForm extends BaseFormType {
  name?: string;
  content?: string;
  file_path?: string;
  imgage_path?: string;
}
