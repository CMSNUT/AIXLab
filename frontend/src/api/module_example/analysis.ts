import request from "@/utils/request";

const API_PATH = "/example/analysis";

const ExampleAnalysisAPI = {
  // 列表查询
  listExampleAnalysis(query: ExampleAnalysisPageQuery) {
    return request<ApiResponse<PageResult<ExampleAnalysisTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailExampleAnalysis(id: number) {
    return request<ApiResponse<ExampleAnalysisTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createExampleAnalysis(body: ExampleAnalysisForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateExampleAnalysis(id: number, body: ExampleAnalysisForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteExampleAnalysis(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchExampleAnalysis(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportExampleAnalysis(query: ExampleAnalysisPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateExampleAnalysis() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importExampleAnalysis(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default ExampleAnalysisAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface ExampleAnalysisPageQuery extends PageQuery {
  name?: string;
  field?: string;
  category?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface ExampleAnalysisTable extends BaseType {
  name?: string;
  field?: string;
  category?: string;
  image?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface ExampleAnalysisForm extends BaseFormType {
  name?: string;
  field?: string;
  category?: string;
  image?: string;
}
