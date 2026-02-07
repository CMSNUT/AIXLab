import request from "@/utils/request";

const API_PATH = "/example/section_programs";

const ExampleSectionProgramsAPI = {
  // 列表查询
  listExampleSectionPrograms(query: ExampleSectionProgramsPageQuery) {
    return request<ApiResponse<PageResult<ExampleSectionProgramsTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailExampleSectionPrograms(id: number) {
    return request<ApiResponse<ExampleSectionProgramsTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createExampleSectionPrograms(body: ExampleSectionProgramsForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateExampleSectionPrograms(id: number, body: ExampleSectionProgramsForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteExampleSectionPrograms(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchExampleSectionPrograms(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportExampleSectionPrograms(query: ExampleSectionProgramsPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateExampleSectionPrograms() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importExampleSectionPrograms(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default ExampleSectionProgramsAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface ExampleSectionProgramsPageQuery extends PageQuery {
  node_id?: string;
  program_id?: string;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface ExampleSectionProgramsTable extends BaseType {
  node_id?: number;
  program_id?: number;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface ExampleSectionProgramsForm extends BaseFormType {
  node_id?: number;
  program_id?: number;
}
