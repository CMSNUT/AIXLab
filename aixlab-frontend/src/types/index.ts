// 认证相关类型
export interface User {
  id: number
  username: string
  email: string
  avatar?: string
  role: 'user' | 'admin'
  created_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  confirmPassword: string
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  timestamp: string
}

// 数据集相关类型
export interface Dataset {
  id: number
  name: string
  description?: string
  file_name: string
  file_size: number
  file_type: string
  columns: DatasetColumn[]
  row_count: number
  is_public: boolean
  user_id: number
  created_at: string
  updated_at: string
}

export interface DatasetColumn {
  name: string
  type: string
  nullable: boolean
  sample_data: any[]
}

export interface DatasetUploadRequest {
  name: string
  description?: string
  is_public: boolean
  file: File
}

// 分析任务相关类型
export interface AnalysisTask {
  id: number
  name: string
  type: 'r' | 'python'
  status: 'pending' | 'running' | 'completed' | 'failed'
  progress: number
  dataset_id: number
  parameters: Record<string, any>
  result?: AnalysisResult
  error_message?: string
  user_id: number
  created_at: string
  updated_at: string
  completed_at?: string
}

export interface AnalysisResult {
  id: number
  task_id: number
  output_text?: string
  output_file?: string
  visualizations: Visualization[]
  statistics: Record<string, any>
  created_at: string
}

export interface Visualization {
  type: string
  title: string
  data: any
  config?: Record<string, any>
}

export interface AnalysisRequest {
  dataset_id: number
  analysis_type: string
  parameters: Record<string, any>
}