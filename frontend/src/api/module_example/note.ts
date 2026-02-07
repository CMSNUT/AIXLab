import request from "@/utils/request";

const API_PATH = "/example/note";

const ExampleNoteAPI = {
  // 列表查询
  listExampleNote(query: ExampleNotePageQuery) {
    return request<ApiResponse<PageResult<ExampleNoteTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailExampleNote(id: number) {
    return request<ApiResponse<ExampleNoteTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createExampleNote(body: ExampleNoteForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateExampleNote(id: number, body: ExampleNoteForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteExampleNote(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchExampleNote(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportExampleNote(query: ExampleNotePageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateExampleNote() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importExampleNote(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default ExampleNoteAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface ExampleNotePageQuery extends PageQuery {
  name?: string;
  description?: string;
  analysis_id?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface ExampleNoteTable extends BaseType {
  name?: string;
  analysis_id?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface ExampleNoteForm extends BaseFormType {
  name?: string;
  analysis_id?: string;
}
